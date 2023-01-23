from sqlalchemy import TIMESTAMP,Column,String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSON
from models import BaseModel
from sqlalchemy.sql import func
from uuid import uuid4 
from sqlalchemy.orm import relationship


class ModelMapping:
    MODEL_MAPPING_TEMPLATE ={
        "modelId":"model_id",
        "manufacturerId":"manufacturer_id",
        "modelName":"model_name",
        "otherDetails":"other_details",
        "createdBy":"created_by",
        "createdOn":"created_on",
        "updatedBy":"updated_by",
        "updatedOn":"updated_on"
    }

class Models(BaseModel):
    __tablename__ = "models"

    model_id = Column(UUID(as_uuid=True),primary_key = True,default = uuid4)
    manufacturer_id = Column(UUID(as_uuid=True),ForeignKey("manufacturer.manufacturer_id"), nullable = False)
    model_name = Column(String(length=200),nullable = False)
    other_details = Column(JSON,nullable = True)
    created_by = Column(String(length=200),nullable = False)
    created_on = Column(TIMESTAMP(timezone=False),server_default = func.now(),nullable = False)
    updated_by = Column(String(length=200),nullable = False)
    updated_on = Column(TIMESTAMP(timezone=False),server_default = func.now(),nullable = False,onupdate=func.now())

    
    manufacturer = relationship("Manufacturer",back_populates = "models")
    vehicles = relationship("Vehicles",back_populates = "models")

    def post_model(self,request_payload):
        mapping = ModelMapping()
        for k, v in request_payload.items():
            setattr(self,mapping.MODEL_MAPPING_TEMPLATE[k],v)
    def get_payload(self):
        return{
            "modelId":str(self.model_id),
            "manufacturer":self.manufacturer.get_payload(),
            "modelName":self.model_name,
            "otherDetails":self.other_details,
            "createdBy":self.created_by,
            "createdOn":str(self.created_on),
            "updatedBy":self.updated_by,
            "updatedOn":str(self.updated_on)
        }
