# main.py
from fastapi import FastAPI
from app.routers import user, auth, material
from app.database import Base, engine


# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Instância do FastAPI
app = FastAPI()

# Registrar as rotas
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(material.router)

@app.get("/")
def root():
    """Rota raiz"""
    return {"message": "Bem-vindo ao sistema CME!"}
