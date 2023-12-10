import os
import re
import sqlite3
import datetime

from calendar import monthrange
from datetime import timedelta, date
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from studio_app.helpers import log_user_in, log_user_out, login_required, validate_password, page_not_found, does_user_exist, not_loged_only, admin_only

app = Flask(
                __name__,
                static_url_path='', 
                static_folder='../studio_app/static/',
                template_folder='../studio_app/templates/'
                )

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_FILE_THRESHOLD'] = 250
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=90)
Session(app)

app.register_error_handler(404, page_not_found)



# Define lists of navbar items to be used in templates
navbar_items = ["Appointments", "Account", "Pricing", "Articles", "Contact", "About", "LogOut"]
navbar_items_not_loged_in = ["Pricing", "Articles", "Contact", "About", "SignIn", "SignUp"]
navbar_items_admin = ["Appointments", "Account", "Clients", "Windows", "Generate_slots", "Pricing", "Articles", "Contact", "About", "LogOut"]

@app.context_processor
def inject_navbar_items():
    return dict(navbar_menu=navbar_items)

@app.context_processor
def inject_navbar_items_not_loged_in():
    return dict(navbar_menu_not_loged_in=navbar_items_not_loged_in)

@app.context_processor
def inject_navbar_items_admin():
    return dict(navbar_items_admin=navbar_items_admin)

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

@app.route("/generate_slots/", methods = ["GET", "POST"])
@login_required
@admin_only
def generate_slots():
    if request.method == "POST":
        try:
            month = int(request.form.get("month"))
            year = int(request.form.get("year"))
        except Exception as er:
            print("#generate: request.form")

        days_slots = [[10, 0], [10, 30], [11, 0], [11, 30], [12, 0], [13, 0], [13, 30], [14, 0], [14, 30], [15, 0]]

        try:
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
        except Exception as er:
            print("#generate: db connection")
        else:
            #check if this month generated
            count_lines = cur.execute("SELECT COUNT(*) FROM calendar WHERE year=? AND month=?", (year, month)).fetchone()[0]
            if not count_lines == 0:
                print("#month exists; count != 0")
                print(count_lines)
                return redirect("/")

        
        days_in_month = monthrange(year, month)[1]

        for day in range(1, days_in_month+1):
            for time in days_slots:
                # calendar (slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT)
                cur.execute("INSERT INTO calendar (year, month, day, hour, minute, is_open) VALUES (?, ?, ?, ?, ?, ?)", (year, month, day, time[0], time[1], 0))
                con.commit()
        
        con.close()
        return redirect("/")

    else:
        return render_template("generate_slots.html")

@app.route("/pricing/")
def pricing():
    return render_template("pricing.html")

@app.route("/signin/", methods = ["GET", "POST"])
@not_loged_only
def signin():
    if request.method == "POST":
        try:

            login = request.form.get("login")
            password = request.form.get("password")
            remember = request.form.get("remember")

            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            print("###remember")
            print(remember)
            if not log_user_in(login, password, cur):
                return render_template("apology.html", error_message="wrong login or passwor")                

        except Exception as er:
            print("### ERROR signin: request.form, db")
            print(er)
            return render_template("apology.html", error_message="Soomething went wrong")

        con.close()
        return redirect("/")

    else:
        return render_template("signin.html")
    

@app.route("/signup/", methods = ["GET", "POST"])
@not_loged_only
def signup():

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
                return render_template("apology.html", error_message="Something went wrong. Try again or contact us. SignUp")
        else:
            return render_template("signup.html")
    except Exception as er:
        print("### ERROR signup: request.form, validation")
        print(er)
        return render_template("apology.html", error_message="Something went wrong.")
    else:         
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        if does_user_exist(login, cur):            
            error_message = "Email " + login + " already registred, try restore password instead."
            con.close()
            return render_template("apology.html", error_message=error_message)
        #insert new user to db
        cur.execute("INSERT INTO users (is_admin, is_clerck, email, lang, instagram, tel, is_subscribed_promo) values (?, ?, ?, ?, ?, ?, ?)", (0, 0, login, "en", instagram, tel_number, 1))
        user_id = cur.execute("SELECT user_id FROM users WHERE login=?", (login,)).fetchone()[0]
        password_hash = generate_password_hash(password)
        cur.execute("INCERT INTO login (user_id, hash) VALUES (?, ?)", (user_id, password_hash))

        log_user_in(login, password, cur)
        con.commit()
        con.close()       
        
        return redirect("/")
    
@app.route("/logout/")
@login_required
def logout():
    log_user_out()
    return redirect("/")

@app.route("/windows/", methods = ["GET", "POST"])
@login_required
@admin_only
def windows():
    # slots = [[1, 2], [3, 4]]
    if request.method == "POST":
        minute = int(request.form.get("minute"))
        hour = int(request.form.get("hour"))
        day = int(request.form.get("date"))
        month = int(request.form.get("month"))
        year = int(request.form.get("year"))
        print("##windows")
        print(hour)
        print(minute)
        print(day)
        print(month)
        print(year)
        return redirect("/windows/")

    else:
        today = datetime.datetime.now()
        try:
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            # slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT
            slots_db = cur.execute("SELECT slot_id, year, month, day, hour, minute, is_open FROM calendar WHERE year>=? AND month>=?", (today.year, today.month)).fetchall()
            slots = []
            for slot in slots_db:
                slots.append(list(slot))
            print(slots)
        except Exception as er:
            slots = None
            print("##/windows/")
            print(er)
        return render_template("windows.html", slots=slots)
