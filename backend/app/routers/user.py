from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.utils import get_password_hash, get_current_active_admin, get_current_active_user
from typing import List  # Import necessário para definir listas nos response models

router = APIRouter(prefix="/users", tags=["users"])

# Rota para criação de usuário (somente administrador pode criar usuários)
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_admin)):
    # Verificar se o email já existe
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Criar novo usuário
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Rota para obter todos os usuários (somente administrador pode acessar)
@router.get("/all", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_admin)):
    users = db.query(models.User).all()
    return users

# Rota para obter informações do usuário atual (acessível por qualquer usuário autenticado)
@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

