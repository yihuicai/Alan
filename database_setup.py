import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base=declarative_base()

class User(Base):
    __tablename__='User'
    Id=Column(Integer, primary_key = True)
    name=Column(String(10), nullable = False)
    profile=Column(String(200), nullable = True)
    email=Column(String(50), nullable = True)

class Catagory(Base):
    __tablename__='Catagory'
    Id=Column(Integer, primary_key = True)
    user_id=Column(Integer, ForeignKey('User.Id'))
    name=Column(String(50), nullable = False)
    
class Item(Base):
    __tablename__='Item'
    Id=Column(Integer, primary_key = True)
    name=Column(String(50), nullable = False)
    attribute=Column(String(50), nullable = True)
    description=Column(String(150), nullable = True)
    url_link=Column(String(200), nullable = True)
    catagory_id=Column(Integer, ForeignKey('Catagory.Id'))
    user_id=Column(Integer, ForeignKey('User.Id'))
    catagory=relationship(Catagory)
    
engine=create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)