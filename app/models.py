from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from .database import Base
from sqlalchemy.sql.expression import text



class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,nullable= False , index=True)
    title = Column(String, nullable= False)
    content = Column(String , nullable= False)
    published = Column(Boolean, server_default = "True" , ullable= False) #PostgreSQL default value karar veriyor
    created_at = Column(DateTime, server_default = text("now()") , nullable= False) 

    ##Inner joine'e de bk relationship