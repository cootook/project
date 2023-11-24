from flask import Flask
from flask import render_template
from datetime import datetime
from . import app

navbar_items = ["Appointments", "Account", "Pricing", "Contact", "About", "LogOut"]
navbar_items_not_loged_in = ["Pricing", "Contact", "About", "SignIn", "SignUp"]

@app.context_processor
def inject_navbar_items():
    return dict(navbar_menu=navbar_items)

@app.context_processor
def inject_navbar_items_not_loged_in():
    return dict(navbar_menu_not_loged_in=navbar_items_not_loged_in)

@app.route("/")
def home():
    is_loged_in = 1
    return render_template("index.html", 
                           is_loged_in = is_loged_in)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")
