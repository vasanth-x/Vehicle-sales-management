from sqlalchemy import Column,String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4 
from models import BaseModel 

class Country(BaseModel):

    __tablename__ = "country"
     
    uuid = Column(UUID(as_uuid= True),primary_key = True, default = uuid4)
    country_code = Column(String(length = 2),nullable = False)
    country_name = Column(String(length = 60),nullable = False)

    address = relationship("Address",back_populates="country")

    def get_payload(self):
        return{
            "countryuuid":str(self.uuid),
            "countryCode":self.country_code,
            "countryName":self.country_name
        }