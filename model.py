from datetime import datetime
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask import *
from passlib.apps import custom_app_context as pwd_context
Base = declarative_base()

class Business(Base):
	__tablename__='business'
	id=Column(Integer, primary_key=True)
	name=Column(String)
	phone=Column(String)
	email=Column(String, unique=True)
	city=Column(String)
	zipcode=Column(String)
	address=Column(String)
	category=Column(String)
	owners=relationship('Owner',back_populates='businesses')


class Owner(Base):
	__tablename__='owner'
	id=Column(Integer, primary_key=True)
	username=Column(String)
	name=Column(String)
	phone=Column(String)
	email=Column(String, unique=True)
	dob=Column(Date)
	businesses=relationship('Business',back_populates='businesses')
	hash_password=Column(String)

	def hash_password(self, password):
		self.hash_password = pwd_context.encrypt(password)

	def verify_password(self, spassword):
		return pwd_context.verify(password, self.hash_password)

