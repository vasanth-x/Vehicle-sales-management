from sqlalchemy import TIMESTAMP,Column,String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSON,DOUBLE_PRECISION,INTEGER
from models import BaseModel
from sqlalchemy.sql import func
from uuid import uuid4 
from sqlalchemy.orm import relationship

class VehicleMapping:
    VEHICLE_MAPPING_TEMPLATE = {
        "vehicleId":"vehicle_id",
        "modelId":"model_id",
        "vehicleStatus":"vehicle_status_code",
        "currentPrice":"current_price",
        "currentMileage":"current_mileage",
        "dateReceived":"date_received",
        "dateOfManufacture":"date_of_manufacture",
        "otherDetails":"other_details",
        "createdBy":"created_by",
        "createdOn":"created_on",
        "updatedBy":"updated_by",
        "updatedOn":"updated_on"
    }
class Vehicles(BaseModel):
    __tablename__ = "vehicles"

    vehicle_id = Column(UUID(as_uuid=True), primary_key = True, default = uuid4)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.model_id"), nullable = False)
    vehicle_status_code = Column(String(length=20), ForeignKey("vehicle_status_code.vehicle_status_code"))
    current_price = Column(INTEGER,nullable = True)
    current_mileage = Column(DOUBLE_PRECISION, nullable = True)
    date_received = Column(TIMESTAMP(timezone= False), nullable = True)
    date_of_manufacture = Column(TIMESTAMP(timezone= False), nullable = True)
    other_details = Column(JSON, nullable = True)
    created_by = Column(String(length = 120), nullable = False)
    created_on = Column(TIMESTAMP(timezone= False), server_default = func.now(), nullable = False)
    updated_by = Column(String(length = 120), nullable = False)
    updated_on = Column(TIMESTAMP(timezone= False), server_default = func.now(), nullable = False,onupdate = func.now())

    models = relationship("Models",back_populates = "vehicles")
    vehicle_status_code_options = relationship("VehicleStatusCode",back_populates = "vehicles")

    def post_vehicle(self,request_payload):
        mapping = VehicleMapping()
        for k, v in request_payload.items():
            if k == "vehicleStatus":
                setattr(self,mapping.VEHICLE_MAPPING_TEMPLATE[k],v["vehicleStatusCode"])    
            else:
                setattr(self,mapping.VEHICLE_MAPPING_TEMPLATE[k],v)

    def get_payload(self):
        return {
            "vehicleId":str(self.vehicle_id),
            "modelId":self.models.get_payload(),
            "vehicleStatusCode":self.vehicle_status_code_options.get_payload(),
            "currentPrice":self.current_price,
            "currentMileage":self.current_mileage,
            "dataReceived":str(self.date_received),
            "dataOfManufacture":str(self.date_of_manufacture),
            "otherDetails":self.other_details,
            "createdBy":self.created_by,
            "createdOn":str(self.created_on),
            "updatedBy":self.updated_by,
            "updatedOn":str(self.updated_on)
        }