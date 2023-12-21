import re
import sqlite3
import datetime

from calendar import monthrange
from datetime import timedelta, date
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from studio_app.helpers import log_user_in, log_user_out, login_required, validate_password, page_not_found, does_user_exist, not_loged_only, admin_only
from .rout_handlers import *

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
navbar_items = ["Appointments", "History", "Account", "Pricing", "Articles", "Contact", "About", "LogOut"]
navbar_items_not_loged_in = ["Pricing", "Articles", "Contact", "About", "SignIn", "SignUp"]
navbar_items_admin = ["All_appointments", "All_history", "Account", "Clients", "Windows", "Generate_slots", "Pricing", "Articles", "Contact", "About", "LogOut"]
days_slots = [[10, 0], [10, 30], [11, 0], [11, 30], [12, 0], [13, 0], [13, 30], [14, 0], [14, 30], [15, 0]]

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
    today = datetime.datetime.now()
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        # slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT
        slots_db = cur.execute("SELECT slot_id, year, month, day, hour, minute, is_open FROM calendar WHERE year>=? AND is_open=1", (today.year,)).fetchall()
          
    except Exception as er:
        con.close()
        slots = None
        print("##/")
        print(er)
        return render_template("apology.html", error_message="Something went wrong.")
    else:
        con.close()
        slots = []
        for slot in slots_db:
            slots.append(list(slot))
        return render_template("index.html", slots=slots)

@app.route("/about/")
def about():    
    return render_template("about.html")

@app.route("/account/", methods=["GET", "POST"])
@login_required
def _account():
    print(request.form.get("tel"))
    return account.account()



@app.route("/apology/")
def apology():
    return render_template("apology.html")

@app.route("/appointments/", methods=["GET", "POST"])
@login_required
def appointments():
    today = datetime.datetime.now()
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        # calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT);
        # appointments (id INTEGER PRIMARY KEY, user_id INT, service_name TEXT, slot_id INT, amount_time_min INT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id));
        user_appoint_db = cur.execute("SELECT id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month=? AND day>=?);", (session.get("user_id"), today.year, today.month, today.day)).fetchall()
        user_appoint_db = user_appoint_db + cur.execute("SELECT id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month>?);", (session.get("user_id"), today.year, today.month)).fetchall()
        user_appoint_db = user_appoint_db + cur.execute("SELECT id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE year>?);", (session.get("user_id"), today.year,)).fetchall()
        user_appoint = []
        for appointment in user_appoint_db:
            if appointment[5] == 0:
                slot_db = list(cur.execute("SELECT year, month, day, hour, minute FROM calendar WHERE slot_id=?", (appointment[2],)).fetchone())
                appointment_as_list = []
                for el in appointment:
                    el = 'No data' if el == None else el
                    appointment_as_list.append(el)
                appointment_as_list = appointment_as_list + slot_db
                user_appoint.append(appointment_as_list)
        user_appoint_sorted = sorted(user_appoint, key = lambda x: (x[7], x[8], x[9], x[10], x[11]))
    except Exception as er:
        con.close()
        print("##/appointments/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
       

    if request.method == "POST":
        try:
            appointment_id_to_cancel = int(request.form.get("appointment_id"))
            print("canceled appointment, id:")
            print(appointment_id_to_cancel)

            cur.execute("UPDATE appointments SET is_canceled=1 WHERE id=?", (appointment_id_to_cancel,))
            con.commit()
            con.close()
            return redirect("/appointments/")

        except Exception as er:
            con.close()
            print("##/appointments/ --cancell")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")

    return render_template("appointments.html", user_appoint=user_appoint_sorted)


@app.route("/all_appointments/", methods=["GET", "POST"])
@login_required
@admin_only
def all_appointments():
    today = datetime.datetime.now()
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        # calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT);
        # appointments (id INTEGER PRIMARY KEY, user_id INT, service_name TEXT, slot_id INT, amount_time_min INT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id));
        user_appoint_db = cur.execute("SELECT user_id, id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month=? AND day>=?) OR slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month>?) OR slot_id IN (SELECT slot_id FROM calendar WHERE year>?);", (today.year, today.month, today.day, today.year, today.month, today.year)).fetchall()
        #user_appoint_db = user_appoint_db + cur.execute("SELECT user_id, id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month>?);", (today.year, today.month)).fetchall()
        #user_appoint_db = user_appoint_db + cur.execute("SELECT user_id, id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE slot_id IN (SELECT slot_id FROM calendar WHERE year>?);", (today.year,)).fetchall()
        user_appoint = []
        for appointment in user_appoint_db:
            if appointment[6] == 0:
                slot_db = list(cur.execute("SELECT year, month, day, hour, minute FROM calendar WHERE slot_id=?", (appointment[3],)).fetchone())
                appointment_as_list = []
                for el in appointment:
                    el = 'No data' if el == None else el
                    appointment_as_list.append(el)
                appointment_as_list = appointment_as_list + slot_db
                user_appoint.append(appointment_as_list)
        user_appoint_sorted = sorted(user_appoint, key = lambda x: (x[8], x[9], x[10], x[11], x[12]))
    except Exception as er:
        con.close()
        print("##/all_appointments/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
       

    if request.method == "POST":
        try:
            # appointment_id_to_cancel = int(request.form.get("appointment_id"))
            return redirect("/all_appointments/")

        except Exception as er:
            con.close()
            print("##/all_appointments/ --edit")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")

    return render_template("all_appointments.html", user_appoint=user_appoint_sorted)


@app.route("/articles/")
def articles():
    return render_template("articles.html")

@app.route("/book/", methods=["GET", "POST"])
@login_required
def book():
    if request.method == "POST":
        try:
            minute = int(request.form.get("minute"))
            hour = int(request.form.get("hour"))
            day = int(request.form.get("date"))
            month = int(request.form.get("month")) + 1 # in calendar.js month range starts from 0
            year = int(request.form.get("year"))
            #calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT);
            #appointments (id INTEGER PRIMARY KEY, user_id INT, service_name TEXT, slot_id INT, amount_time_min INT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id));
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            slot_to_book = cur.execute("SELECT slot_id, is_open FROM calendar WHERE year=? AND month=? AND day=? AND hour=? AND minute=?;", (year, month, day, hour, minute)).fetchone()
            is_open = True if slot_to_book[1] == 0 else False
            slot_id = slot_to_book[0]
            cur.execute("UPDATE calendar SET is_open=0 WHERE slot_id=?;", (slot_id,))
            cur.execute("INSERT INTO appointments (user_id, slot_id, is_seen, is_aproved, is_canceled, amount_time_min) VALUES (?, ?, 0, 0, 0, 120);", (session.get("user_id"), slot_id))
            con.commit()
            con.close()
            return redirect("/")
        
        except Exception as er:
            con.close()
            print("##/book/ --request.form.get, db query")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")        

    else:
        return redirect("/")


@app.route("/clients/", methods=["GET", "POST"])
@login_required
@admin_only
def clients():
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        # users (id INTEGER PRIMARY KEY, is_admin INT, is_clerck INT ,  name TEXT, email TEXT, lang TEXT, instagram TEXT, tel TEXT, is_subscribed_promo INT, avatar TEXT)
        clients_db = cur.execute("SELECT name, instagram, tel, email FROM users").fetchall()
        clients = list()
        for client in clients_db:
            client_new = list()
            for el in client:
                el = "-" if el == None else el
                client_new.append(el)
            clients.append(client_new) 
        print(clients)
    except Exception as er:
        con.close()
        print("##/clients/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
       

    if request.method == "POST":
        try:
            # appointment_id_to_cancel = int(request.form.get("appointment_id"))
            return redirect("/clients/")

        except Exception as er:
            con.close()
            print("##/clients/ --edit")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")

    return render_template("clients.html", clients=clients)


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

@app.route("/history/")
@login_required
def history():
    today = datetime.datetime.now()
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        # calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT);
        # appointments (id INTEGER PRIMARY KEY, user_id INT, service_name TEXT, slot_id INT, amount_time_min INT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id));
        user_appoint_db = cur.execute("SELECT id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month=? AND day<?);", (session.get("user_id"), today.year, today.month, today.day)).fetchall()
        user_appoint_db = user_appoint_db + cur.execute("SELECT id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month<?);", (session.get("user_id"), today.year, today.month)).fetchall()
        user_appoint_db = user_appoint_db + cur.execute("SELECT id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE year<?);", (session.get("user_id"), today.year,)).fetchall()
        user_appoint = []
        for appointment in user_appoint_db:
            
            slot_db = list(cur.execute("SELECT year, month, day, hour, minute FROM calendar WHERE slot_id=?", (appointment[2],)).fetchone())
            appointment_as_list = []
            for el in appointment:
                el = 'No data' if el == None else el
                appointment_as_list.append(el)
            appointment_as_list = appointment_as_list + slot_db
            user_appoint.append(appointment_as_list)
                # (id - 7, service_name - None, slot - 252, seen - 0, aproved - 0, canceled - 1, timing - 120, 2023, 12, 27, 11, 30)
        print(user_appoint)
        user_appoint_sorted = sorted(user_appoint, key = lambda x: (x[9], x[8], x[7], x[10], x[11]))
    except Exception as er:
        con.close()
        print("##/history/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
       
    return render_template("history.html", user_appoint=user_appoint_sorted)

@app.route("/all_history/", methods = ["GET", "POST"])
@login_required
@admin_only
def all_history():
    today = datetime.datetime.now()
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()        
        # calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT);
        # appointments (id INTEGER PRIMARY KEY, user_id INT, service_name TEXT, slot_id INT, amount_time_min INT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id));
        user_appoint_db = cur.execute("SELECT id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min, user_id FROM appointments WHERE slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month=? AND day<?);", (today.year, today.month, today.day)).fetchall()
        user_appoint_db = user_appoint_db + cur.execute("SELECT id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min, user_id FROM appointments WHERE slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month<?);", (today.year, today.month)).fetchall()
        user_appoint_db = user_appoint_db + cur.execute("SELECT id, service_name, slot_id, is_seen, is_aproved, is_canceled, amount_time_min, user_id FROM appointments WHERE slot_id IN (SELECT slot_id FROM calendar WHERE year<?);", (today.year,)).fetchall()
        user_appoint = []
        for appointment in user_appoint_db:
            
            slot_db = list(cur.execute("SELECT year, month, day, hour, minute FROM calendar WHERE slot_id=?", (appointment[2],)).fetchone())
            appointment_as_list = []
            for el in appointment:
                el = 'No data' if el == None else el
                appointment_as_list.append(el)
            appointment_as_list = appointment_as_list + slot_db
            user_appoint.append(appointment_as_list)
                # (id - 7, service_name - None, slot - 252, seen - 0, aproved - 0, canceled - 1, timing - 120, 2023, 12, 27, 11, 30)
        print(user_appoint)
        user_appoint_sorted = sorted(user_appoint, key = lambda x: (x[9], x[8], x[7], x[10], x[11]))
    except Exception as er:
        con.close()
        print("##/all_history/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
       

    if request.method == "POST":
        try:
            # appointment_id_to_cancel = int(request.form.get("appointment_id"))

            return redirect("/all_history/")

        except Exception as er:
            con.close()
            print("##/all_history/ --edit")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")

    return render_template("all_history.html", user_appoint=user_appoint_sorted)

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
        try:       
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            if does_user_exist(login, cur):            
                error_message = "Email " + login + " already registred, try restore password instead."
                con.close()
                return render_template("apology.html", error_message=error_message)
            #insert new user to db
            cur.execute("INSERT INTO users (is_admin, is_clerck, email, lang, instagram, tel, is_subscribed_promo) values (?, ?, ?, ?, ?, ?, ?)", (0, 0, login, "en", instagram, tel_number, 1))
            user_id = cur.execute("SELECT id FROM users WHERE email=?", (login,)).fetchone()[0]
            password_hash = generate_password_hash(password)
            cur.execute("INSERT INTO login (user_id, hash) VALUES (?, ?)", (user_id, password_hash))
        except Exception as er:
            print("###/signup/ --insert new user to db")
            print(er)
            con.close()
            return render_template("apology.html", error_message="Something went wrong. Try again or contact us.") 
        else:
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
    if request.method == "POST":
        try:
            minute = int(request.form.get("minute"))
            hour = int(request.form.get("hour"))
            day = int(request.form.get("date"))
            month = int(request.form.get("month")) + 1 # in calendar.js month range starts from 0
            year = int(request.form.get("year"))

            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            slot_to_edit = cur.execute("SELECT slot_id, is_open FROM calendar WHERE year=? AND month=? AND day=? AND hour=? AND minute=?;", (year, month, day, hour, minute)).fetchone()
            new_is_open = 1 if slot_to_edit[1] == 0 else 0
            cur.execute("UPDATE calendar SET is_open=? WHERE slot_id=?", (new_is_open, slot_to_edit[0]))
            con.commit()
            con.close()
            return redirect("/windows/")

        except Exception as er:
            print("##/windows/ --request.form.get, db query")
            print(er)
            return render_template("apology.html", error_message="Something went wrong.")
        
        

    else:
        today = datetime.datetime.now()
        try:
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            # slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT
            slots_db = cur.execute("SELECT slot_id, year, month, day, hour, minute, is_open FROM calendar WHERE year>=?", (today.year,)).fetchall()
            slots = []
            for slot in slots_db:
                slots.append(list(slot))
            con.close()
        except Exception as er:
            con.close()
            slots = None
            print("##/windows/")
            print(er)
        return render_template("windows.html", slots=slots)
