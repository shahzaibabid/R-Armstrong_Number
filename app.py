from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
 return render_template("index.html")

@app.route("/about")
def about():
 return render_template("about-us.html")

@app.route("/contact")
def contact():
 return render_template("contact.html")

@app.route("/feedback")
def feedback():
 return render_template("feedback.html")

@app.route("/signin")
def signin():
 return render_template("signin.html")

@app.route("/register")
def register():
 return render_template("register.html")

app.run(debug=True)