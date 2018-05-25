import os
import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'User_orm'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    fullname = Column(String)
    email = Column(String)
    password = Column(String)
    nfc_id = Column(Integer)
    user_flow = Column(Integer)
    
    
class Keg(Base):
    __tablename__ = 'Keg_orm'
    id = Column(Integer, primary_key=True)
    keg_id = Column(Integer)
    keg_flow = Column(Integer)
    
    
path_to_database = "BeerBase.db"    
engine = create_engine('sqlite:///'+path_to_database)

Base.metadata.create_all(engine)