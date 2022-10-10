from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base




class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,nullable= False , index=True)
    title = Column(String, nullable= False)
    content = Column(String , nullable= False)
    published = Column(Boolean, server_default = "True" , nullable= False) #PostgreSQL default value karar veriyor
    created_at = Column(TIMESTAMP(timezone=True), server_default = text("now()") , nullable= False) 
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable= False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,nullable= False , index=True)
    name = Column(String, nullable= False)
    email = Column(String, nullable= False, unique=True) # Her kullanıcı aynı email ile bir kezqeydiyyatdan keçə bilər
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), server_default = text("now()") , nullable= False) 

