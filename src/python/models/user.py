from sqlalchemy import Column,String,Boolean
from models import BaseModel

class User(BaseModel):

    __tablename__ = "users"

    email = Column(String(length=100),primary_key = True,nullable = False)
    password = Column(String(length=60),nullable = False)
    is_admin = Column(Boolean,nullable = False)