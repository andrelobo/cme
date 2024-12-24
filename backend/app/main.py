# main.py
from fastapi import FastAPI
from app.routers import user, auth  # Importando os módulos de rotas
from app.database import Base, engine, get_db
from app.models import User
from app.utils import get_password_hash
from sqlalchemy.orm import Session
import os

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Instância do FastAPI
app = FastAPI()

# Registrar as rotas
app.include_router(user.router)
app.include_router(auth.router)

import logging

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_default_admin():
    """Cria um usuário administrativo padrão se ele não existir"""
    logger.info("Executando a função create_default_admin...")
    db: Session = next(get_db())  # Obtém a sessão do banco de dados
    admin_email = os.getenv("ADMIN_EMAIL", "admin@cme.com")  # Email padrão do admin
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # Senha padrão
    admin_role = "admin"

    # Verificar se o admin já existe
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    if not existing_admin:
        hashed_password = get_password_hash(admin_password)  # Gera o hash da senha
        admin = User(
            name="Administrador",
            email=admin_email,
            hashed_password=hashed_password,
            role=admin_role,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        logger.info(f"Usuário admin criado com email: {admin_email} e senha: {admin_password}")
    else:
        logger.info("Usuário admin já existe!")

    """Cria um usuário administrativo padrão se ele não existir"""
    print("Executando a função create_default_admin...")  # Depuração
    db: Session = next(get_db())  # Obtém a sessão do banco de dados
    admin_email = os.getenv("ADMIN_EMAIL", "admin@cme.com")  # Email padrão do admin
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # Senha padrão
    admin_role = "admin"

    # Verificar se o admin já existe
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    if not existing_admin:
        hashed_password = get_password_hash(admin_password)  # Gera o hash da senha
        admin = User(
            name="Administrador",
            email=admin_email,
            hashed_password=hashed_password,
            role=admin_role,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"Usuário admin criado com email: {admin_email} e senha: {admin_password}")
    else:
        print("Usuário admin já existe!")

    """Cria um usuário administrativo padrão se ele não existir"""
    db: Session = next(get_db())  # Obtém a sessão do banco de dados
    admin_email = os.getenv("ADMIN_EMAIL", "admin@cme.com")  # Email padrão do admin
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # Senha padrão
    admin_role = "admin"

    # Verificar se o admin já existe
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    if not existing_admin:
        hashed_password = get_password_hash(admin_password)  # Gera o hash da senha
        admin = User(
            name="Administrador",
            email=admin_email,
            hashed_password=hashed_password,
            role=admin_role,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"Usuário admin criado com email: {admin_email} e senha: {admin_password}")
    else:
        print("Usuário admin já existe!")

# Executar a criação do admin ao iniciar a aplicação
@app.on_event("startup")
def startup_event():
    """Eventos a serem executados ao iniciar a aplicação"""
    create_default_admin()

@app.get("/")
def root():
    """Rota raiz"""
    return {"message": "Bem-vindo ao sistema CME!"}
