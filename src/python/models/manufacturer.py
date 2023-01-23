from sqlalchemy import TIMESTAMP,Column,String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSON
from models import BaseModel
from sqlalchemy.sql import func
from uuid import uuid4 
from sqlalchemy.orm import relationship


class Manufacturer(BaseModel):

    __tablename__ =  "manufacturer"
     
    manufacturer_id = Column(UUID(as_uuid= True), primary_key = True, default = uuid4)
    manufacturer_name = Column(String(length = 200), nullable = False)
    address_id = Column(UUID(as_uuid= True),ForeignKey("address.address_id"),nullable = False)
    email_address = Column(String(length = 60),nullable = False)
    Phone = Column(String(length = 60),nullable = True )
    mobile = Column(String(length = 60),nullable = False)
    other_details = Column(JSON,nullable =True)
    created_by = Column(String(length = 120), nullable = False)
    created_on = Column(TIMESTAMP(timezone= False), server_default = func.now(), nullable = False)
    updated_by = Column(String(length = 120), nullable = False)
    updated_on = Column(TIMESTAMP(timezone= False), server_default = func.now(), nullable = False)

    address = relationship("Address",back_populates = "manufacturer")
    models = relationship("Models",back_populates = "manufacturer")

    def get_payload(self):
        return{
            "manufacturerId":str(self.manufacturer_id),
            "manufactureName":self.manufacturer_name,
            "addressId":self.address.get_payload(),
            "emailAddress":self.email_address,
            "Phone":self.Phone,
            "mobile":self.mobile,
            "otherDetails":self.other_details,
            "created_by":self.created_by,
            "created_on":str(self.created_on),
            "updated_by":self.updated_by,
            "updated_on":str(self.updated_on)
            }