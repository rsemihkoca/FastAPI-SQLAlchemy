from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:8520@localhost/db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#Dependency for database: Create a new session for each request and close it after the request is completed
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def table_exists(name):
    ins = inspect(engine)
    ret = ins.dialect.has_table(engine.connect(),name)
    return ret
