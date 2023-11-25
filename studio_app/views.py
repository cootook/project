from flask import Flask
from flask import render_template
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

#from . import app

#from helpers import log_user_in, login_required

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

@app.route("/account/")
@login_required
def about():
    return render_template("account.html")

@app.route("/appointments/")
@login_required
def about():
    return render_template("appointments.html")

@app.route("/articles/")
def about():
    return render_template("articles.html")

@app.route("/contact/")
def about():
    return render_template("contact.html")

@app.route("/day/")
@login_required
def about():
    return render_template("day.html")

@app.route("/pricing/")
def about():
    return render_template("pricing.html")

@app.route("/signin/")
def about():
    return render_template("signin.html")

@app.route("/signup/")
def about():
    return render_template("signup.html")

