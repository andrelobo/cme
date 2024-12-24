from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

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
