import os
import re
import sqlite3
import datetime
import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from calendar import monthrange
from datetime import timedelta, date
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from studio_app.helpers import log_user_in, log_user_out, login_required, validate_password, page_not_found, does_user_exist, not_loged_only, admin_only, get_service_name
from .rout_handlers import *
# from flask_mail import Mail, Message

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

app.config['MAIL_SERVER'] = 'smtp.yandex.com'
app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_APP_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
# mail = Mail(app)

Session(app)

app.register_error_handler(404, page_not_found)



# Define lists of navbar items to be used in templates
navbar_items = ["Appointments", "History", "Account", "Contact", "LogOut"]
navbar_items_not_loged_in = ["Contact", "SignIn", "SignUp"]
navbar_items_admin = ["All_appointments", "All_history", "Account", "Clients", "Windows", "Generate_slots", "Contact", "LogOut"]
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

# @app.route("/test_mail/", methods=["GET", "POST"])
# @login_required
# def test_mail():
#     recipient = "cootook@gmail.com"
#     msg = Message('Test Email', recipients=[recipient])
#     msg.body = ('Congratulations! You have sent a test email with '
#                 'Yandex')
#     msg.html = ('<h1>Test Email</h1>'
#                 '<p>Congratulations! You have sent a test email with '
#                 '<b>Yandex</b>!</p>')
#     mail.send(msg)
#     flash(f'A test message was sent to {recipient}.')
#     return redirect("/")


@app.route("/test_mail_py/", methods=["GET", "POST"])
@login_required
def test_mail_py():
    mail_server = os.environ.get('MAIL_SERVER')
    receiver = "cootook@gmail.com"
    sender = "matveising@ya.ru"
    port = os.environ.get('MAIL_PORT')
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

    with smtplib.SMTP_SSL("smtp.yandex.com", port, context=context) as server:
        server.login(username, password)
        server.sendmail(sender, receiver, message.as_string())

    # msg = EmailMessage()
    # msg.set_content("test message python")

    # # me == the sender's email address
    # # you == the recipient's email address
    # msg['Subject'] = f'Test of sending'
    # msg['From'] = "cootook@gmail.con"
    # msg['To'] = "matveising@ya.ru"

    # # Send the message via our own SMTP server.
    # s = smtplib.SMTP("127.0.0.1")

    # username = os.environ.get('MAIL_USERNAME')
    # password = os.environ.get('MAIL_APP_KEY')
    # server = smtplib.SMTP('smtp.yandex.com:465')
    # server.ehlo()
    # server.starttls()
    # server.login(username,password)
    # server.sendmail(fromaddr, toaddrs, msg)
    # server.quit()

    # s.send_message(msg)
    # s.quit()


    flash(f'A test message was sent to {receiver}.')
    return redirect("/")


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
def _signup():
    return signup.signup()
# def signup():

#     try:
#         if request.method == "POST":
#             instagram = request.form.get("instagram")
#             tel_number = request.form.get("tel_number")
#             login = request.form.get("login")
#             password = request.form.get("password")
#             confirmation = request.form.get("confirmation")

#             is_pass_ok = (password == confirmation) and validate_password(password)
#             is_instagram_ok = len(instagram) >= 3
#             is_tel_ok = len(tel_number) >= 10
#             regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
#             is_login_ok = (re.fullmatch(regex_email, login) != None)

#             if not is_pass_ok or not is_instagram_ok or not is_tel_ok or not is_login_ok:
#                 return render_template("apology.html", error_message='''
#                                        Password must contain:</br>
#                                        - a lowercase letter</br>
#                                        - a capital (uppercase) letter</br>
#                                        - a number</br>
#                                        - minimum 6 characters.</br>
#                                        </br>
#                                        Instagramm name should be valid.</br>
#                                         </br>
#                                        Telephone at leats 10 digits.</br>
#                                         </br>
#                                        Email adress.</br>
#                                        ''')
#         else:
#             return render_template("signup.html")
#     except Exception as er:
#         print("### ERROR signup: request.form, validation")
#         print(er)
#         return render_template("apology.html", error_message="Something went wrong.")
#     else:   
#         try:       
#             con = sqlite3.connect("./db.db") 
#             cur = con.cursor()
#             if does_user_exist(login, cur):            
#                 error_message = "Email " + login + " already registred, try restore password instead."
#                 con.close()
#                 return render_template("apology.html", error_message=error_message)
#             #insert new user to db
#             cur.execute("INSERT INTO users (is_admin, is_clerck, email, lang, instagram, tel, is_subscribed_promo) values (?, ?, ?, ?, ?, ?, ?)", (0, 0, login, "en", instagram, tel_number, 1))
#             user_id = cur.execute("SELECT id FROM users WHERE email=?", (login,)).fetchone()[0]
#             password_hash = generate_password_hash(password)
#             cur.execute("INSERT INTO login (user_id, hash) VALUES (?, ?)", (user_id, password_hash))
#         except Exception as er:
#             print("###/signup/ --insert new user to db")
#             print(er)
#             con.close()
#             return render_template("apology.html", error_message="Something went wrong. Try again or contact us.") 
#         else:
#             log_user_in(login, password, cur)
#             con.commit()
#             con.close()            
#             return redirect("/")
    
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
            return  render_template("apology.html", error_message="Something went wrong")
        return render_template("windows.html", slots=slots)
