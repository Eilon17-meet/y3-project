from flask import *
from flask import session as login_session
from model import *
from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

@app.route('/')
def home():
	owner=None
	if 'id' in login_session:
		owner=session.query(Owner).filter_by(id=login_session['id']).first()
	return render_template('home.html', owner=owner)

@app.route('/login')
def login():
	if 'id' in login_session:
		flash("You are already logged in")
		return redirect(url_for('home'))
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username == "" or password == "":
			flash("Missing Arguements")
			return redirect(url_for('login'))

		owner = session.query(Owner).filter_by(username=username).first()
		if not owner:
			flash("Incorrect password / email combination")
			return redirect(url_for('login'))
		elif verify_password(owner.username, password): 
			flash('Login Successful. Welcome, %s' %user.firstname)
			login_session['username']= owner.username
			login_session['name'] = owner.name
			login_session['email'] = owner.email
			login_session['id'] = owner.id
			return redirect(url_for('home'))


@app.route('/logout', methods = ['POST'])
def logout():
	if 'id' not in login_session:
		flash("You must be logged in order to log out")
		return redirect(url_for('home'))
	del login_session['username']
	del login_session['name']
	del login_session['email']
	del login_session['id']
	flash("Logged out successfully")
	return redirect(url_for('home'))




@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		name = request.form['name']
		phone = request.form['phone']
		email = request.form['email']
		dob = request.form['dob']
		password = request.form['password']
		confirmpassword = request.form['confirmpassword']
		if username == "" or name == "" or phone == "" or email == "" or dob == "" or  password == "" or confirmpassword == "" :
			flash("Your form is missing arguments")
			return redirect(url_for('signup'))
		if session.query(Owner).filter_by(username=username). first() is not None:
			flash("A user with this email address already exists")
			return redirect(url_for('signup')) 
		user = User(username=username,name=name, email=email, dob=dob, phone=phone)
		user.hash_password(password)
		session.add(user)
		session.commit()
		flash("User created successfully")
		return redirect(url_for('login'))
	else:
		return render_template('signup.html')










if __name__ == '__main__':
	app.run(debug=True)