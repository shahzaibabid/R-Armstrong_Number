from flask import Flask, render_template,request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
import json
pymysql.install_as_MySQLdb()

with open('config.json','r') as c:
    params=json.load(c)['params']

app = Flask(__name__)

local_server=True

# ============================ database connectivity =======================


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/python-flask'
db = SQLAlchemy(app)
app.secret_key='super-secret-key'

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



@app.route("/signin")
def signin():
    posts=Post.query.filter_by().all()
    return render_template("signin.html",params=params,posts=posts)

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

# user routes

@app.route("/user",  methods = ['GET','POST'])
def user():


    
    if ('user' in session and session ['user'] == params['admin_user']):
        posts=Post.query.all()
        return render_template('dashboard.html',params=params,posts=posts)
        
    
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if (email == params['admin_user'] and password == params['admin_password']):
            #set the session variable
            session['user']= email
            posts=Post.query.all()
            return render_template('user.html',params=params,posts=posts)
            
            
        
    
    return render_template('login.html',params=params)


@app.route("/profile")
def profile():
    return render_template("profile.html")



@app.route("/calculatearmstrong")
def calculatearmstrong():
    return render_template("calculatearmstrong.html")



@app.route("/calculaterange")
def calculaterange():
    return render_template("calculaterange.html")


@app.route("/signout")
def signout():
    return render_template("signout.html")

# @app.route("/signout")
# def signout():
#    session.pop('user ') 
#    return redirect('/user.html')

app.run(debug=True)