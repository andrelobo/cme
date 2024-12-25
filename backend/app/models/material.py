# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# Model para Material
class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    expiration_date = Column(Date, nullable=False)
    serial = Column(String, unique=True, nullable=False)  # Serial gerado automaticamente

    # Relacionamento com tracking
    tracking_records = relationship("MaterialTracking", back_populates="material")


# Model para Tracking de Material
class MaterialTracking(Base):
    __tablename__ = "material_tracking"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    step = Column(String, nullable=False)  # Etapa do processo
    date = Column(Date, nullable=False)  # Data da etapa
    failed_attempts = Column(Integer, default=0)  # Falhas ocorridas na etapa

    # Relacionamento com Material
    material = relationship("Material", back_populates="tracking_records")
