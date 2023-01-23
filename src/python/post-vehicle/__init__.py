import os
from service.DBinit import DB

db_name = os.environ['DB_NAME']
host_name = os.environ['DB_HOSTNAME']
pwd = os.environ['DB_PASSWORD']
uname = os.environ['DB_USERNAME']
port = os.environ['DB_PORT']
schema= os.environ['DB_SCHEMA']

db = DB(
    user=uname,
    password=pwd,
    host=host_name,
    database=db_name,
    port = port,
    schema=schema
)

Session = db.getSession()