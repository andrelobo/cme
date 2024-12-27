from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.utils import get_password_hash, get_current_active_admin, get_current_active_user
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

# Rota para criação de usuário (somente administrador pode criar usuários)
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_admin)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
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

# Rota para obter informações de um usuário pelo ID (somente administrador pode acessar)
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# Rota para atualizar um usuário pelo ID (somente administrador pode atualizar usuários)
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.name = user_update.name or user.name
    user.email = user_update.email or user.email
    user.role = user_update.role or user.role
    if user_update.password:
        user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(user)
    return user

# Rota para deletar um usuário pelo ID (somente administrador pode deletar usuários)
@router.delete("/{user_id}", response_model=schemas.UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(user)
    db.commit()
    return user
