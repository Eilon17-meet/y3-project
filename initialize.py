from model import *
from datetime import *

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

session.query(Business).delete()


example_business_password='Business_Password_123'
for i in xrange(1,3):
	example_business= Business(
		name="Falafel "+str(i),
		phone='052423545',
		email=str(i),
		city='Haifa',
		address='Hashalom 13',
		zipcode='12345',
		category='food',
		stat_id=i)

	example_business.hash_password(example_business_password)

	session.add(example_business)

for i in xrange(1,3):
	example_stat=Stat(
		date=datetime.now(),
		start_hour=7,
	    finish_hour=20,
	    employees_amount=5,
	    customers_amount=120,
	    cost=540.5,
	    earnings=1090.2,
	    business_id=i
	)
	session.add(example_stat)

session.commit()