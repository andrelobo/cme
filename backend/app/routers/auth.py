from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.utils import verify_password, create_access_token
from app.schemas.user import LoginRequest, LoginResponse  # Importando diretamente do user.py

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)  # Usando diretamente LoginResponse
def login(request: LoginRequest, db: Session = Depends(get_db)):  # Usando diretamente LoginRequest
    # Verificar se o usuário existe
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Verificar se a senha está correta
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Criar o token de acesso
    access_token = create_access_token(data={"sub": user.email})
    
    return LoginResponse(access_token=access_token)
