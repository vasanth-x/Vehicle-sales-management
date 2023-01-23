from sqlalchemy import TIMESTAMP,Column,String
from models import BaseModel
from sqlalchemy.sql import func
from uuid import uuid4 
from sqlalchemy.orm import relationship


class VehicleStatusCode(BaseModel):

    __tablename__ = "vehicle_status_code"

    vehicle_status_code = Column(String(length=20), primary_key = True, nullable = False)
    description = Column(String(length = 200),nullable = False)

    vehicles = relationship("Vehicles",back_populates = "vehicle_status_code_options")

    def get_payload(self):
        return {
            "vehicleStatusCode":self.vehicle_status_code,
            "description":self.description
        }