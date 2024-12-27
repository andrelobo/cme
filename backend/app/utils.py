import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

# Configuração do contexto para hash de senhas com o Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 para obter o token do cabeçalho Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Use uma chave secreta forte
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # O algoritmo a ser utilizado para a assinatura do token
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Tempo de expiração do token

# Função para gerar um hash da senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar se a senha em texto puro corresponde ao hash armazenado
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar um token de acesso (JWT)
def create_access_token(data: dict, expires_delta: timedelta = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar e decodificar o token JWT
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Função para buscar um usuário pelo email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Função para criar o usuário administrador se não existir
def create_admin_user(db: Session):
    admin_email = "admin@cme.com"
    user = get_user_by_email(db, admin_email)
    if not user:
        admin_user = models.User(
            name="Administrador", 
            email=admin_email, 
            role="admin",
            hashed_password=get_password_hash("admin123")  # Exemplo de senha, mude conforme necessário
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Administrador criado")
    else:
        print("Administrador já existe")

# Função para verificar e decodificar o token JWT e retornar o usuário atual
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Função para verificar se o usuário é ativo (com papel de 'user')
def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Ação não permitida para este papel")
    return current_user

# Função para verificar se o usuário é administrador (com papel de 'admin')
def get_current_active_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Ação não permitida para administradores")
    return current_user
