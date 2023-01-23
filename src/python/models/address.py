from sqlalchemy import TIMESTAMP,Column,String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSON,INTEGER
from sqlalchemy.sql import func
from uuid import uuid4 
from models import BaseModel
from sqlalchemy.orm import relationship




class Address(BaseModel):

    __tablename__ = "address"


    address_id = Column(UUID(as_uuid=True),primary_key = True,nullable= False,default = uuid4)
    door_no = Column(String(length = 30),nullable= False)
    address_line_1 = Column(String(length = 60),nullable= False)
    address_line_2 = Column(String(length=60),nullable = True)
    place = Column(String(length = 30),nullable= False)
    city = Column(String(length = 50),nullable= False)
    zipcode = Column(INTEGER,nullable = False)
    latitude = Column(String(length = 30), nullable = True)
    longitude = Column(String(length = 30), nullable = True)
    country_code = Column(UUID(as_uuid = True),ForeignKey('country.uuid'),nullable= False)
    other_details = Column(JSON, nullable =True)
    created_by = Column(String(length = 120), nullable = False)
    created_on = Column(TIMESTAMP(timezone= False), server_default = func.now(), nullable = False)
    updated_by = Column(String(length = 120), nullable = False)
    updated_on = Column(TIMESTAMP(timezone= False), server_default = func.now(), nullable = False)

    country = relationship("Country",back_populates="address")
    manufacturer = relationship("Manufacturer",back_populates="address")

    def get_payload(self):
        return {
            "addressId":str(self.address_id),
            "doorNo" : self.door_no,
            "address_line_1":self.address_line_1,
            "address_line_2":self.address_line_2,
            "place":self.place,
            "city":self.city,
            "zipcode":self.zipcode,
            "latitude":self.latitude,
            "longitude":self.longitude,
            "country":self.country.get_payload(),
            "otherDetails":self.other_details,
            "createdBy":self.created_by,
            "createdOn":str(self.created_on),
            "updatedby":self.updated_by,
            "updatedOn":str(self.updated_on)
        }
