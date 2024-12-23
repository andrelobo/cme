from fastapi import FastAPI
from app.routers import user
from app.database import Base, engine


# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registrar rotas
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Bem-vindo ao sistema CME!"}
