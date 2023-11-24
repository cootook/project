from flask import Flask
from flask import render_template
from datetime import datetime
from . import app

navbar_items = ["Appointments", "Account", "Pricing", "Contact", "About", "LogOut"]

@app.context_processor
def inject_navbar_items():
    return dict(navbar_menu=navbar_items)

@app.route("/")
def home():
    loged_in = 1
    return render_template("index.html", loged_in=loged_in)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")