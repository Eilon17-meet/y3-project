from model import *
from datetime import *

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

session.query(Business).delete()
session.query(Stat).delete()


example_business_password='password'
example_business= Business(
	name="Falafel",
	owner_name='Rihana',
	phone='+97256937304',
	email='email',
	facebook_link='https://www.facebook.com/boost.hq/', # Our  facebook page
	instagram_link='https://www.instagram.com/boost.hq/', #Our instagram page
	city='Haifa',
	address='Hashalom 13',
	zipcode='34652',
	category='food')

example_business.hash_password(example_business_password)

session.add(example_business)

for i in xrange(1,3):
	example_stat=Stat(
		
		#start_hour=7,
	    #finish_hour=20,
	    #employees_amount=5,
	    customers_amount=120,
	    #cost=540.5,
	    earnings=1090.2,
	    business_id=1
	)
	session.add(example_stat)

session.commit()