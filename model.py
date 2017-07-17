from datetime import *
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask import *
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
Base = declarative_base()

# DELETE OWNER CLASS AND MAKE STATISTIC DATABASE
class Stat(Base):
    """Statistic info of each date"""
    id = Column(Integer, primary_key=True)
    date=Column(Date) #datetime.now()
    start_hour=Column(Integer)
    finish_hour=Column(Integer)
    employees_amount=Column(Integer)
    customers_amount=Column(Integer)
    cost=Column(Float)
    earnings=Column(Float)
    
    '''
    -Opening hours
-Amount of employees
-Amount of customers
-Daily costs
-Earnings'''

class Owner(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    dob = Column(Date) #Date of birth
    city = Column(String)
    address = Column(String)
    zipcode = Column(String)
    business = relationship("Business", back_populates="owner")


class Business(Base):
    __tablename__ = 'business'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True) #Thats how you log in
    password_hash = Column(String)      #Thats how you log in
    city = Column(String)
    address = Column(String)
    zipcode = Column(String)
    category = Column(String)
    #comments = relationship("Comment", back_populates="business") #Not yet here
    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship("Owner", back_populates="business")

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)



engine = create_engine('sqlite:///database.db')


Base.metadata.create_all(engine)
