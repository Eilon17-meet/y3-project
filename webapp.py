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

def verify_password(email, password):
    #print '##################\n'+email+'\t'+password+'\n##############'
    business = session.query(Business).filter_by(email=email).first()
    if not business or not business.verify_password(password):
        return False
    g.business = business
    return True

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='GET':
        # owner=None
        if 'id' in login_session:
            business=session.query(Business).filter_by(id=login_session['id']).first()
            return render_template('home.html', business=business)
        return render_template('home.html')
    elif request.method=='POST':
        return redirect(url_for('search', s=request.form['s']))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'id' in login_session:
        flash("You are already logged in, "+login_session['name'])
        return redirect(url_for('business', business_id=login_session['id']))
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == "" or password == "":
            flash("Missing Arguements")
            return redirect(url_for('login'))

        business = session.query(Business).filter_by(email=email).first()
        if business.activated==False:
            flash('Your account wasn\'t activated by Boost managers. For help please contact us.',business.activated)
            return redirect(url_for('home'))
        if verify_password(email, password):
            business = session.query(Business).filter_by(email=email).one()
            login_session['name'] = business.name
            login_session['email'] = business.email
            login_session['id'] = business.id

            flash('Login Successful! Welcome back, %s.' % business.name)
            return redirect(url_for('business'))
        else:
            flash('Incorrect username/password combination')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'id' not in login_session:
        flash("You must be logged in order to log out")
        return redirect(url_for('home'))
    del login_session['name']
    del login_session['email']
    del login_session['id']
    flash("Logged out successfully")
    return redirect(url_for('home'))

'''
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        dob = request.form['dob']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        if name == "" or phone == "" or email == "" or dob == "" or  password == "" or confirmpassword == "" :
            flash("Your form is missing arguments")
            return redirect(url_for('signup'))
        if session.query(Owner).filter_by(eamil=eamil). first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('signup')) 
        user = User(name=name, email=email, dob=dob, phone=phone)
        user.hash_password(password)
        session.add(user)
        session.commit()
        flash("User created successfully")
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')
'''
'''
@app.route('/search/<s>', methods=['GET']) #DELETE AND REPLACE WITH REVIEWS
def search(s):
    search_results=[]
    search_results+=session.query(Business).filter_by(name=str(s)).all()
    search_results+=session.query(Business).filter_by(city=str(s)).all()
    search_results+=session.query(Business).filter_by(address=str(s)).all()
    search_results+=session.query(Business).filter_by(category=str(s)).all()
    for word in str(s).split():
        word=word.capitalize()
        search_results+=session.query(Business).filter_by(name=word).all()
        search_results+=session.query(Business).filter_by(city=word).all()
        search_results+=session.query(Business).filter_by(address=word).all()
        search_results+=session.query(Business).filter_by(category=word).all()
    return render_template('search_results.html',search_results=search_results, search_term=s)'''

@app.route('/business/', methods=['GET','POST'])
def business():
    business=session.query(Business).filter_by(id=login_session['id']).one()
    if request.method=='GET':
        return render_template('business_profile.html', business=business)
    elif request.method=='POST':
        if 'id' not in login_session:
            flash('You have to login in order to see this information.')
            return redirect(url_for('login'))
        date=request.form['date']
        customers_amount=request.form['customers_amount']
        earnings=request.form['earnings']
        stat=Stat(
            date=date,
            customers_amount=customers_amount,
            earnings=earnings,
            business_id=login_session['id']
            )
        session.add(stat)
        session.commit()

@app.route('/stats/', methods=['GET'])
def stats():
    if 'id' not in login_session:
        flash('You have to login in order to see this information.')
        return redirect(url_for('login'))
    business=session.query(Business).filter_by(id=login_session['id']).one()
    return render_template('stats.html', business=business)

@app.route('/signup/', methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    elif request.method=='POST':
        name=request.form['name']
        owner_name=request.form['owner_name']
        phone=request.form['phone']
        email=request.form['email']
        password=request.form['password']
        facebook_link=request.form['facebook_link']
        instagram_link=request.form['instagram_link']
        city=request.form['city']
        address =request.form['address']
        category=request.form['category']
        about=request.form['about']
        website=request.form['website']
        print('abt to make business in DB')
        business=Business(
            name=name,
            owner_name=owner_name,
            phone=phone,
            email=email,
            facebook_link=facebook_link,
            instagram_link=instagram_link,
            city=city,
            address=address,
            category=category,
            about=about,
            activated=False,
            website=website)
        business.hash_password(password)
        session.add(business)
        session.commit()
        return redirect(url_for('home')) 

# @app.route('/owner', methods=['GET'])
# def owner():
#     if 'id' not in login_session:
#         flash("You must be logged in order to preform this action")
#         return redirect(url_for('login'))
    
#     owner=session.query(Business).filter_by(id=login_session['id']).all()
#     return render_template('owner_profile.html', owner=owner)




if __name__ == '__main__':
    app.run(debug=True)