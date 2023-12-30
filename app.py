from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
 return render_template("index.html")

@app.route("/about")
def about():
 return render_template("about-us.html")

@app.route("/contact_us")
def contact():
 return render_template("contacts.html")

app.run(debug=True)