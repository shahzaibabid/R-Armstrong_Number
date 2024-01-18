from flask import Flask, render_template,request, session, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
currentDateAndTime = datetime.now()
import pymysql
import json
import hashlib
import math

pymysql.install_as_MySQLdb()

with open('config.json','r') as c:
    params=json.load(c)['params']

app = Flask(__name__)

local_server=True

# ============================ database connectivity =======================

app.secret_key='super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/python-flask'
db = SQLAlchemy(app)
#================classes=====================

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False , nullable=True)
    email = db.Column(db.String(120), unique=True) 
    rating = db.Column(db.String(120), unique=True, nullable=False)
    improve = db.Column(db.String(120), unique=True , nullable=False )

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False , nullable=True)
    username = db.Column(db.String(100), unique=False , nullable=True)
    email = db.Column(db.String(120), unique=True) 
    phone = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True , nullable=False )
    
@app.route("/")
def index():
 return render_template("index.html")

@app.route("/about")
def about():
 return render_template("about-us.html")

@app.route("/contact")
def contact():
 return render_template("contact.html")

@app.route("/feedback", methods=["GET","POST"])
def feedback():
    if(request.method=="POST"):
        
        name = request.form.get('name')
        email = request.form.get('email')
        rating = request.form.get('rating')
        improve = request.form.get('improve')
        
        entry = Feedback(name = name, email=email,rating=rating,improve=improve)
        db.session.add(entry)
        db.session.commit()
        

    
    
    return render_template("feedback.html", params=params)



@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Query the database for the user with the provided email
        user = Register.query.filter_by(email=email).first()

        if user and user.password == password:
            # User exists and password is correct, set session and redirect to profile
            session["user_id"] = user.id  # Store the user's ID in the session
            return redirect(url_for("profile"))
        else:
            # User does not exist or password is incorrect, render login page with error message
            return render_template("signin.html", error="Invalid email or password")

    # If the request method is GET, render the login page
    return render_template("signin.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if(request.method=="POST"):
        
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        entry = Register(name = name, username=username, email=email, phone=phone, password=password)
        db.session.add(entry)
        db.session.commit()
        return redirect("signin")
           
    return render_template("register.html", params=params)

#================== user routes======================

@app.route("/user",  methods = ['GET','POST'])
def user():
 
    return render_template('user.html')
        


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" in session:
        user_id = session["user_id"]
        user = Register.query.get(user_id)

        if user:
            return render_template("profile.html", user=user)
        else:
            return "User not found", 404
    else:
        return redirect(url_for("signin"))

@app.route("/edit_profile", methods=['GET', 'POST'])
def editprofile():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phoneNumber']

        user_id = session["user_id"]

        user = Register.query.get(user_id)

        user.name = name
        user.phone = phone

        db.session.commit()

        return redirect(url_for('profile'))

    else:
        user_id = session["user_id"]
        user = Register.query.get(user_id)

        if user:
            return render_template("editprofile.html", user=user, post=user)
        else:
            return "User not found", 404
        
@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        user_id = session["user_id"]

        user = Register.query.get(user_id)

        if new_password == confirm_password:
            user.password = new_password

            db.session.commit()

            return redirect(url_for('profile'))
        else:
            return "New password and confirmation do not match"

    else:
        return render_template("changepassword.html")
        
def is_armstrong_number(num):
    order = len(str(num))
    total = 0
    temp = num
    while temp > 0:
        digit = temp % 10
        total += digit ** order
        temp //= 10
    return num == total

def is_valid_input(num):
    return 0 <= num <= 99999

@app.route("/calculatearmstrong", methods=['GET', 'POST'])
def calculatearmstrong():
    if 'counter' not in session:
        session['counter'] = 0

    result = None
    error_message = None

    if request.method == 'POST':
        try:
            number = int(request.form['number'])
            if is_valid_input(number):
                result = is_armstrong_number(number)
                session['counter'] += 1

                if session['counter'] == 5:
                    return redirect(url_for('register'))
            else:
                error_message = "Please enter a number between 0 and 99999."
        except ValueError:
            error_message = "Invalid input. Please enter a valid number."
    return render_template("calculatearmstrong.html", result=result, error_message=error_message)


def is_Armstrong(val):
    armstrong_numbers = []
    for num in range(val[0], val[1] + 1):
        sum = 0
        order = len(str(num))
        temp = num
        while temp > 0:
            digit = temp % 10
            sum += digit ** order
            temp //= 10
        if num == sum:
            armstrong_numbers.append(num)
    return armstrong_numbers

def is_Armstrong(num):
    armstrong_numbers = []
    for number in range(num[0], num[1] + 1):
        order = len(str(number))
        total = 0
        temp = number
        while temp > 0:
            digit = temp % 10
            total += digit ** order
            temp //= 10
        if number == total:
            armstrong_numbers.append(number)
    return armstrong_numbers

@app.route("/calculaterange", methods=["GET", "POST"])
def calculaterange():
    if request.method == "POST":
        starting_range = int(request.form["starting_range"])
        ending_range = int(request.form["ending_range"])
        range_values = (starting_range, ending_range)
        armstrong_numbers = is_Armstrong(range_values)
        return render_template("calculaterange.html", armstrong_numbers=armstrong_numbers)
    return render_template("calculaterange.html")


@app.route("/signout")
def signout():
    if 'users' in session:
        session.pop('users')
    return redirect('/signin')



#================== Admin panel routes======================



#======== User Route =====


@app.route("/auser", methods=["GET" , "POST"])
def auser():
    posts=Register.query.filter_by().all()
    return render_template("auser.html" , params=params , posts=posts)


#======== Feedback Route =====

@app.route("/afeedback" , methods=["GET" , "POST"])
def afeedback():
    
    posts=Feedback.query.filter_by().all()
    return render_template("afeedback.html",params=params , posts=posts)

#======== user attempt Route =====

@app.route("/auserattempt")
def auserattempt():
    

    return render_template("auserattempt.html",params=params)

#=======dashboard route=============
@app.route("/aindex")
def aindex():
    
    posts=Feedback.query.all()
    post1=Register.query.all()
    return render_template("aindex.html", params=params, posts=posts,post1=post1)
#======== Login =====

@app.route("/admin",  methods = ['GET','POST'])
def dashboard():
    
    posts=Feedback.query.all()
    post1=Register.query.all()
    
    
    if ('user' in session and session ['user'] == params['admin_user']):
        # posts=Login.query.all()
        return render_template('aindex.html',params=params,posts=posts,post1=post1)
        
    
    if request.method=='POST':
        username = request.form.get('email')
        userpass = request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_password']):
            #set the session variable
            session['user']= username
            # posts=Login.query.all()
            return render_template('aindex.html',params=params,posts=posts,post1=post1)
            
            
        
    
    return render_template('alogin.html',params=params)



#======== Logout =====

@app.route("/alogout")
def logout():
    
    session.pop('user')
    return redirect('/admin')


app.run(debug=True)