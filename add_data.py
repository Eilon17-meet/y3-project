from model import *
from datetime import *
from random import *
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

for i in range(10):
	example_stat=Stat(
		
		#start_hour=7,
	    #finish_hour=20,
	    #employees_amount=5,
	    customers_amount=int(i*i*0.2),
	    #cost=540.5,
	    earnings=uniform(1000,2000)*i,
	    business_id=1
	)
	session.add(example_stat)

session.commit()