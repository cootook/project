import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from studio_app.helpers import log_user_in, log_user_out, login_required

app = Flask(
                __name__,
                static_url_path='', 
                static_folder='../studio_app/static/',
                template_folder='../studio_app/templates/'
                )

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define lists of navbar items to be used in templates
navbar_items = ["Appointments", "Account", "Pricing", "Articles", "Contact", "About", "LogOut"]
navbar_items_not_loged_in = ["Pricing", "Articles", "Contact", "About", "SignIn", "SignUp"]

@app.context_processor
def inject_navbar_items():
    return dict(navbar_menu=navbar_items)

@app.context_processor
def inject_navbar_items_not_loged_in():
    return dict(navbar_menu_not_loged_in=navbar_items_not_loged_in)

@app.route("/")
def home():
    is_loged_in = 0
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/account/")
@login_required
def account():
    return render_template("account.html")

@app.route("/appointments/")
@login_required
def appointments():
    return render_template("appointments.html")

@app.route("/articles/")
def articles():
    return render_template("articles.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/day/")
@login_required
def day():
    return render_template("day.html")

@app.route("/pricing/")
def pricing():
    return render_template("pricing.html")

@app.route("/signin/")
def signin():
    log_user_in("Bilbo Sumkin", "1")
    return redirect("/")

@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/logout/")
def logout():
    log_user_out()
    return redirect("/")
