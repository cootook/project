import atexit
import os
import re
import secrets
import sqlite3
import datetime
import smtplib, ssl
import time
import flask_security

from apscheduler.schedulers.background import BackgroundScheduler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from calendar import monthrange
from datetime import timedelta, date
from flask import Flask, flash, redirect, render_template, request, session, render_template_string
from flask_mailman import Mail
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.forms import LoginForm, ConfirmRegisterForm
from flask_session import Session
from jinja2 import Environment as jinja2_env
from .helpers import validate_recaptcha
from studio_app.forms import ExtendedRegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select
from studio_app.config import ProductionConfig, DevelopmentConfig, TestingConfig
from studio_app.db_classes import db_base
from studio_app.db_classes import Appointment, Booking_message, Language, Notification_type, Payment, Payment_method, Payment_status, Payment_type, Role, Service, Service_role, Slot, User, User_notification, User_role
from studio_app.helpers import log_user_in, log_user_out, login_required, validate_password, page_not_found, does_user_exist, not_loged_only, admin_only, get_service_name
from .rout_handlers import *

# flask security
from typing import List

app = Flask(
                __name__,
                static_url_path='', 
                static_folder = os.environ.get('FLASK_STATIC_FOLDER'),
                template_folder = os.environ.get('FLASK_TEMPLATE_FOLDER')
                )

### configuration selection
# app.config.from_object(ProductionConfig)
app.config.from_object(DevelopmentConfig)
# app.config.from_object(TestingConfig)

Session(app)
mail = Mail(app)

db_base.init_app(app)

with app.app_context():
    # db_base.drop_all()  

    db_base.create_all()

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db_base, User, Role)
app.security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)

app.register_error_handler(404, page_not_found)

# Define lists of navbar items to be used in templates
navbar_items = ["Appointments", "History", "Account", "Contact", "LogOut"]
navbar_items_not_loged_in = ["Contact", "SignIn", "SignUp"]
navbar_items_admin = ["All_appointments", "All_history", "Account", "Clients", "Windows", "Generate_slots", "Contact", "LogOut"]
days_slots = [[10, 0], [10, 30], [11, 0], [11, 30], [12, 0], [13, 0], [13, 30], [14, 0], [14, 30], [15, 0]]

jinja2_env.SITE_KEY_RECAPTCHA = os.environ.get('SITE_KEY_RECAPTCHA')

@app.context_processor
def set_site_key_recaptcha():
    return {"SITE_KEY_RECAPTCHA": os.environ.get('SITE_KEY_RECAPTCHA')}

@app.context_processor
def inject_navbar_items():
    return dict(navbar_menu=navbar_items)

@app.context_processor
def inject_navbar_items_not_loged_in():
    return dict(navbar_menu_not_loged_in=navbar_items_not_loged_in)

@app.context_processor
def inject_navbar_items_admin():
    return dict(navbar_items_admin=navbar_items_admin)

@app.route("/test_mail_py/", methods=["GET", "POST"])
@login_required
def test_mail_py():
    mail_server = os.environ.get('MAIL_SERVER')

    receiver = "cootook@gmail.com"
    sender = "matveising@ya.ru"
    port = int(os.environ.get('MAIL_PORT'))
    username = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_APP_KEY')

    message = MIMEMultipart("alternative")
    # message.set_content("This message is sent from Python.")
    message['Subject'] = 'Test of sending via Python'
    message['To'] = "cootook@gmail.con"
    message['From'] = "Liza nail studio <matveising@ya.ru>"

    text = """\
    Hi,
    This is a plain text.
    """
    html = """\
    <html>
    <body>
        <p>Hi,<br>
        Second one
        This is HTML<br>
        <a href="https://github.com/cootook">my GitHub</a> 
        </p>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(mail_server, port, context=context) as server:
        server.login(username, password)
        server.sendmail(sender, receiver, message.as_string())

    flash(f'A test message was sent to {receiver}.')
    return redirect("/")


@app.route("/test/")
# @auth_required()
def test():
    return render_template_string("Hello {{ current_user.email }}")

@app.route('/register', methods=['GET', 'POST'])
# @register_view
def register():
    if request.method == 'POST':
    # email: Mapped[str] = mapped_column(unique = True)
    # password: Mapped[Optional[str]]
    # login_count: Mapped[int] 
    # name: Mapped[str]   
    # instagram: Mapped[str] 
    # tel: Mapped[Optional[str]]
        email = request.form.get('email')
        password = request.form.get('password')
        login_count = 0
        name = request.form.get('name')
        instagram = request.form.get('instagram')
        tel = request.form.get('tel')
        
        user_datastore.create_user(email = email, password = hash_password(password))
        db_base.commit()
    return render_template('security/register_user.html')

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
    return account.account()

@app.route("/apology/")
def apology():
    return render_template("apology.html")

@app.route("/appointments/", methods=["GET", "POST"])
@login_required
def _appointments():
    return appointments.appointments()

@app.route("/all_appointments/", methods=["GET"])
@login_required
@admin_only
def _all_appointments():
    return all_appointments.all_appointments()

@app.route("/articles/")
def articles():
    return render_template("articles.html")

@app.route("/book/", methods=["GET", "POST"])
@login_required
def _book():
    return book.book()



@app.route("/cancel_appointment/", methods = ["POST"])
@login_required
def _cancel_appointment():
    return cancel_appointment.cancel_appointment()


@app.route("/change_password/", methods = ["GET", "POST"])
@login_required
def _change_password():
    return change_password.change_password()


@app.route("/change_role/", methods = ["GET", "POST"])
@login_required
def _change_role():
    return change_role.change_role()


@app.route("/clients/", methods=["GET", "POST"])
@login_required
@admin_only
def clients():
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        # users (id INTEGER PRIMARY KEY, is_admin INT, is_clerck INT ,  name TEXT, email TEXT, lang TEXT, instagram TEXT, tel TEXT, is_subscribed_promo INT, avatar TEXT)
        clients_db = cur.execute("SELECT name, instagram, tel, email, id FROM users").fetchall()
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


@app.route("/confirm_appointment/", methods = ["POST"])
@login_required
@admin_only
def _confirm_appointment():
    return confirm_appointment.confirm_appointment()


@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/day/")
@login_required
def day():
    return render_template("day.html")


@app.route("/done_appointment/", methods = ["POST"])
@login_required
@admin_only
def _done_appointment():
    return done_appointment.done_appointment()

@app.route("/edit_appointment/", methods=["POST"])
@login_required
@admin_only
def _edit_appointment():
    return edit_appointment.edit_appointment()

@app.route("/generate_slots/", methods = ["GET", "POST"])
@login_required
@admin_only
def generate_slots():
    if request.method == "POST":
        try:
            month = int(request.form.get("month"))
            year = int(request.form.get("year"))
            print("###")
            print(month, year)
        except Exception as er:
            print("##/generate_slots/ request.form")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")        

        try:
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
        except Exception as er:
            print("##/generate_slots/ -dbm")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")
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
def _history():
    return history.history()

@app.route("/all_history/", methods = ["GET", "POST"])
@login_required
@admin_only
def _all_history():
    return all_history.all_history()

@app.route("/pricing/")
def pricing():
    return render_template("pricing.html")

@app.route("/signin/", methods = ["GET", "POST"])
@not_loged_only
def signin():
    if request.method == "POST":
        try:
            token = request.form.get("g-recaptcha-response")
            login = request.form.get("login")
            password = request.form.get("password")
            remember = request.form.get("remember")

            if not validate_recaptcha(token):
                return  render_template("apology.html", error_message="Sorry. Something went wrong with anti robot protection. Please, try again or contact us.")


            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            print("###remember")
            print(remember)
            if not log_user_in(login, password, cur):
                return render_template("apology.html", error_message="wrong login or password")                

        except Exception as er:
            print("### ERROR signin: request.form, db")
            print(er)
            return render_template("apology.html", error_message="Something went wrong")

        con.close()
        return redirect("/")

    else:
        return render_template("signin.html")
    

@app.route("/signup/", methods = ["GET", "POST"])
@not_loged_only
def _signup():
    return signup.signup()
    
@app.route("/logout/")
@login_required
def logout():
    log_user_out()
    return redirect("/")

@app.route("/windows/", methods = ["GET", "POST"])
@login_required
@admin_only
def windows():
    db_v2_slots = Slot.query.filter().all()
    slots_to_frontend = []
    for s in db_v2_slots:
        slots_to_frontend.append([s.id, s.date.year, s.date.month, s.date.day, s.time.hour, s.time.minute, 1 if s.opened else 0])

    if request.method == "POST":
        try:
            target_slot_id = int(request.form.get("slot-id"))
            minute = int(request.form.get("minute"))
            hour = int(request.form.get("hour"))
            day = int(request.form.get("date"))
            month = int(request.form.get("month")) + 1 # in calendar.js month range starts from 0
            year = int(request.form.get("year"))

            target_date = datetime.date(year, month, day)
            target_time = datetime.time(hour, minute)

            target_slot = Slot.query.filter(Slot.id == target_slot_id, Slot.date == target_date, Slot.time == target_time).first()

            if target_slot.opened :
                target_slot.opened = False
                target_slot.opened_by_id = None
                target_slot.opened_at = None
            else:
                target_slot.opened = True
                target_slot.opened_by_id = session["user_id"]
                target_slot.opened_at = datetime.datetime.now()

            db_base.session.commit()
            return redirect("/windows/")

        except Exception as er:
            print("##/windows/ --request.form.get, db query")
            print(er)
            return render_template("apology.html", error_message="Something went wrong.")
        
    return render_template("windows.html", slots=slots_to_frontend)
        

with app.app_context():
    Slot.delete_old_empty()
    Slot.create_n_days_upfront(35)
    Slot.create(2023, 10, 5, 11, 30)
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=create_slots_n_days_upfront, trigger="interval", hours=24)
# scheduler.start()

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())