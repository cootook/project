import os
import re
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from studio_app.helpers import log_user_in, log_user_out, login_required, validate_password, page_not_found

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

app.register_error_handler(404, page_not_found)



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

@app.route("/apology/")
def apology():
    return render_template("apology.html")

@app.route("/appointments/")
@login_required
def appointments():
    return render_template("appointments.html")

@app.route("/articles/")
def articles():
    return render_template("articles.html")

@app.route("/book/", methods=["GET", "POST"])
@login_required
def book():
    if request.method == "POST":
        minute = int(request.form.get("minute"))
        hour = int(request.form.get("hour"))
        day = int(request.form.get("date"))
        month = int(request.form.get("month"))
        year = int(request.form.get("year"))
        print(hour)
        print(minute)
        print(day)
        print(month)
        print(year)
        return redirect("/about/")

    else:
        return redirect("/")

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

@app.route("/signin/", methods = ["GET", "POST"])
def signin():
    #log_user_in("Bilbo Sumkin", "1")
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        remember = request.form.get("remember")

        print(login)
        print(password)
        print(remember)

        log_user_in(login, "1")
        
        return redirect("/")

    else:
        return render_template("signin.html")
    

@app.route("/signup/", methods = ["GET", "POST"])
def signup():
    if session.get("user_id") is not None:
        return redirect("/")
    try:
        if request.method == "POST":
            instagram = request.form.get("instagram")
            tel_number = request.form.get("tel_number")
            login = request.form.get("login")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            is_pass_ok = (password == confirmation) and validate_password(password)
            is_instagram_ok = len(instagram) >= 3
            is_tel_ok = len(tel_number) >= 10
            regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            is_login_ok = (re.fullmatch(regex_email, login) != None)

            if not is_pass_ok or not is_instagram_ok or not is_tel_ok or not is_login_ok:
                return render_template("apology.html", error_message="Something went wrong. Try again or contact us.")
        else:
            return render_template("signup.html")
    except:
        return render_template("apology.html", error_message="Something went wrong. Try again or contact us.")
    else:   
        print(instagram)
        print("password is " + "ok" if is_pass_ok else "not ok")
        print("instagram is " + "ok" if is_instagram_ok else "not ok")
        print("tell is " + "ok" if is_tel_ok else "not ok")
        print("login is " + "ok" if is_login_ok else "not ok")
        password_hash = generate_password_hash(password)

        con = sqlite3.connect("./db.db") 
        cur = con.cursor()

        #chek if email exist in db
        is_email_in_db = cur.execute("SELECT COUNT (id) FROM users WHERE email=?;", (login,)).fetchone()[0] == 1
        print(is_email_in_db) # [0]) == 1)
        if is_email_in_db:
            error_message = "Email " + login + " already registred, try restore password instead."
            return render_template("apology.html", error_message=error_message)
        #cur.execute("INSERT INTO users (is_admin, is_clerck, email, lang, instagram, tel, is_subscribed_promo) values (?, ?, ?, ?, ?, ?, ?)", (0, 0, login, "en", instagram, tel_number, 1))

        #con.commit()
        con.close()
        
        log_user_in(instagram, "1")
        return redirect("/")
    
@app.route("/logout/")
def logout():
    log_user_out()
    return redirect("/")
