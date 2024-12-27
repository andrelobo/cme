import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Contexto para hash de senhas com o Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para gerar um hash da senha
def get_password_hash(password: str) -> str:
    """Gera um hash para a senha usando bcrypt."""
    return pwd_context.hash(password)

# Função para verificar se a senha em texto puro corresponde ao hash armazenado
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto puro corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)

# Esquema OAuth2 para obter o token do cabeçalho Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Use uma chave secreta forte
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # O algoritmo a ser utilizado para a assinatura do token
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Tempo de expiração do token

# Função para gerar um token de acesso (JWT)
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Gera o token JWT."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Criação do payload
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    
    # Geração do token JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar e decodificar o token JWT
def verify_token(token: str):
    """Verifica e decodifica o token JWT."""
    try:
        # Decodifica o token usando a chave secreta e o algoritmo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Retorna o conteúdo do payload
    except JWTError:
        return None  # Se o token for inválido ou expirado

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Verifica e decodifica o token JWT, e retorna o usuário atual."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    """Verifica se o usuário tem o papel de 'user' e retorna o usuário ativo."""
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Ação não permitida para este papel")
    return current_user

def get_current_active_admin(current_user: models.User = Depends(get_current_user)):
    """Verifica se o usuário tem o papel de 'admin' e retorna o usuário ativo."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Ação não permitida para administradores")
    return current_user

def get_user_by_email(db: Session, email: str):
    """Busca um usuário pelo email."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_admin_user(db: Session):
    """Cria o usuário administrador se não existir."""
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

# No ponto de inicialização, por exemplo, em main.py:
from fastapi import FastAPI
from app.database import SessionLocal, engine
from app.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    create_admin_user(db)
    db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}
