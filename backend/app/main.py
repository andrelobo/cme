# main.py
# main.py
from fastapi import FastAPI
from app.routers import user, auth, material
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware




# Criar tabelas no banco de dados
# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)


# Instância do FastAPI
# Instância do FastAPI
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Permite o frontend Vite
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os headers
)

# Registrar as rotas
# Registrar as rotas
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(material.router)

@app.get("/")
def root():
    """Rota raiz"""
    """Rota raiz"""
    return {"message": "Bem-vindo ao sistema CME!"}
