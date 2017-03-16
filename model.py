from datetime import datetime
from sqlalchemy import Column, Integer,String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask import *
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
Base = declarative_base()


class Business(Base):
    __tablename__ = 'business'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    city = Column(String)
    zipcode = Column(String)
    address = Column(String)
    category = Column(String)
    owners = relationship('Owner', back_populates='businesses')


class Owner(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    dob = Column(DateTime)
    hash_password = Column(String)
    when_created=Column(DateTime, default=datetime.now())
    businesses = relationship('Business', back_populates='businesses')

    def hash_password(self, password):
        self.hash_password = pwd_context.encrypt(password)

    def verify_password(self, spassword):
        return pwd_context.verify(password, self.hash_password)


engine = create_engine('sqlite:///database.db')


Base.metadata.create_all(engine)
