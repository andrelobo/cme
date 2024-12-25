from pydantic import BaseModel
from datetime import date
from typing import List


# Esquema Base para o rastreamento do material
class MaterialTrackingBase(BaseModel):
    step: str
    date: date
    failed_attempts: int


# Esquema para criar um registro de rastreamento
class MaterialTrackingCreate(MaterialTrackingBase):
    pass


# Esquema de saída para um registro de rastreamento
class MaterialTrackingOut(MaterialTrackingBase):
    id: int  # ID único do registro

    class Config:
        orm_mode = True  # Permite trabalhar com objetos do SQLAlchemy


# Esquema para criar um material
class MaterialCreate(BaseModel):
    name: str  # Nome do material
    type: str  # Tipo do material
    expiration_date: date  # Data de validade


# Esquema de saída para o material
class MaterialOut(BaseModel):
    id: int
    name: str
    type: str
    expiration_date: date
    serial: str  # Serial gerado automaticamente
    tracking_records: List[MaterialTrackingOut] = []  # Rastreamento associado

    class Config:
        orm_mode = True
