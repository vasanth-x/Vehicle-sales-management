from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DB:
    def __init__(self, user=None, password=None, host=None, database=None,port=None, schema=None):
        self.user = user 
        self.password = password
        self.host = host 
        self.port = port
        self.database = database 
        self.connect_timeout = 15
        self.schema = schema 
        db_string = "postgresql://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.database
        )
        self.db = create_engine(
            db_string,
            echo=True,
            connect_args={
                'connect_timeout': self.connect_timeout,
                'options': '-csearch_path={}'.format(self.schema)
            }
        )
        
    def getSession(self):
        return sessionmaker(bind=self.db)