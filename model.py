from datetime import *
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask import *
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
Base = declarative_base()

class Stat(Base):
    __tablename__= 'stat'
    id = Column(Integer, primary_key=True)
    date=Column(Date, default=datetime.now())
    #start_hour=Column(Integer)
    #finish_hour=Column(Integer)
    #employees_amount=Column(Integer)
    customers_amount=Column(Integer)
    #cost=Column(Float)
    earnings=Column(Float)
    business_id=Column(Integer, ForeignKey('business.id'))
    #business = relationship("Business", back_populates="stat")
    

class Business(Base):
    __tablename__ = 'business'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_name=Column(String)
    phone = Column(String)
    email = Column(String, unique=True) #Thats how you log in
    password_hash = Column(String)      #Thats how you log in
    facebook_link=Column(String)
    instagram_link=Column(String)
    city = Column(String)
    address = Column(String)
    category = Column(String)
    about=Column(String) #I am -- from -- and this is my business...
    #comments = relationship("Comment", back_populates="business") #Not yet here
    #stat_id = Column(Integer, ForeignKey('stat.id'))
    website=Column(String)
    stat = relationship("Stat")
    # stat = relationship(Stat
    
    activated=Column(Boolean)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def getEarnings(self):
        dates_list = [s.date for s in self.stat] #make a comment
        money_list = [s.earnings for s in self.stat]
        assert len(dates_list) == len(money_list)
        earnings_over_time = []

        for i in range(len(dates_list)):
            date_money_pair = [dates_list[i],money_list[i]]
            earnings_over_time.append(date_money_pair)


        return earnings_over_time









engine = create_engine('sqlite:///database.db')


Base.metadata.create_all(engine)