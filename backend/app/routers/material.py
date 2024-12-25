from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/materials", tags=["materials"])


# Criar um novo material
@router.post("/", response_model=schemas.MaterialOut)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    # Gerar serial único com base no nome do material
    serial = f"{material.name[:5].upper()}-{db.query(models.Material).count() + 1:03}"
    
    # Criar o objeto do material
    new_material = models.Material(
        name=material.name,
        type=material.type,
        expiration_date=material.expiration_date,
        serial=serial,
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material


# Obter todos os materiais
@router.get("/", response_model=list[schemas.MaterialOut])
def get_all_materials(db: Session = Depends(get_db)):
    materials = db.query(models.Material).all()
    return materials


# Adicionar rastreamento a um material
@router.post("/{material_id}/tracking", response_model=schemas.MaterialTrackingOut)
def add_tracking(
    material_id: int,
    tracking: schemas.MaterialTrackingCreate,
    db: Session = Depends(get_db),
):
    # Verificar se o material existe
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado.")
    
    # Criar registro de rastreamento
    new_tracking = models.MaterialTracking(
        material_id=material_id,
        step=tracking.step,
        date=tracking.date,
        failed_attempts=tracking.failed_attempts,
    )
    db.add(new_tracking)
    db.commit()
    db.refresh(new_tracking)
    return new_tracking


# Obter rastreamento de um material
@router.get("/{material_id}/tracking", response_model=list[schemas.MaterialTrackingOut])
def get_tracking(material_id: int, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado.")
    return material.tracking_records


# Obter informações detalhadas de um material
@router.get("/{material_id}", response_model=schemas.MaterialOut)
def get_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado.")
    return material
