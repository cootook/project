import os
import click
import sqlite3
import datetime
import requests
import flask_security

from calendar import monthrange
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, render_template_string, send_file
from flask.cli import with_appcontext
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password, login_user, verify_and_update_password, logout_user
from flask_security.forms import LoginForm, ConfirmRegisterForm
from flask_session import Session
from jinja2 import Environment as jinja2_env
from .helpers_legacy import validate_recaptcha, validate_twilio_request, send_email
from .helpers.email import Email_service
from studio_app.forms import ExtendedRegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select
from studio_app.config import ProductionConfig, DevelopmentConfig, TestingConfig
from studio_app.db_classes import db_base
from studio_app.db_classes import Appointment, Booking_message, Language, Notification_type, Payment, Payment_method, Payment_status, Payment_type, Role, Service, Service_role, Slot, User, User_notification, User_role
from studio_app.helpers_legacy import log_user_in, log_user_out, login_required, validate_password, page_not_found, does_user_exist, not_loged_only, admin_only, get_service_name
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from .rout_handlers import *


# flask security
from typing import List

load_dotenv()

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
migrate = Migrate(app, db_base)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db_base, User, Role)
app.security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)

app.register_error_handler(404, page_not_found)

# Define lists of navbar items to be used in templates
navbar_items = ["Appointments", "History", "Account", "Contact", "Terms_of_service", "Privacy_policy", "LogOut"]
navbar_items_not_loged_in = ["Contact", "Terms_of_service", "Privacy_policy", "SignIn"]
navbar_items_admin = ["All_appointments", "Add_service", "Account", "Clients", "Windows", "Contact", "Terms_of_service", "Privacy_policy", "LogOut"]
days_slots = [[10, 0], [10, 30], [11, 0], [11, 30], [12, 0], [13, 0], [13, 30], [14, 0], [14, 30], [15, 0]]

jinja2_env.SITE_KEY_RECAPTCHA = os.environ.get('SITE_KEY_RECAPTCHA')

@app.context_processor
def get_services():
    services = []
    services_from_db = db_base.session.scalars(select(Service))
    for service in services_from_db:
        service_dict = dict(id = service.id, name = service.name, description = service.description, deleted = service.deleted)
        services.append(service_dict)
    return dict(services=services)

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

@app.route('/f2c5930a29900498068d74013e18e78c.html', methods=['GET'])
def verify_html():
    return send_file('f2c5930a29900498068d74013e18e78c.html', as_attachment=True)

@app.route('/privacy_policy', methods=['GET'])
@app.route('/privacy_policy/', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/terms_of_service', methods=['GET'])
@app.route('/terms_of_service/', methods=['GET'])
def terms_of_service():
    return render_template('terms_of_service.html')


@app.route('/register', methods=['GET', 'POST'])
# @register_view
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        login_count = 0
        name = request.form.get('name')
        instagram = request.form.get('instagram')
        tel = request.form.get('tel')
        
        user_datastore.create_user(email = email, password = hash_password(password))
        db_base.commit()
    return render_template('security/register_user.html')

@app.route('/test_email/', methods=['GET', 'POST'])
def test_email():
    new_email = Email_service(
        "cootook@gmail.com", 
        "more tests", 
        "Another test email \n https://www.maniaurabyrusa.com/"
        )
    status = new_email.send()
    if status == "OK":
        return redirect('/')
    else:
        return render_template("apology.html", error_message=status)

@app.route('/sms/', methods=['GET', 'POST'])
# @register_view
def sms():
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    new_key = client.new_keys.create(friendly_name="test sms")

    message = client.messages.create(
        body="visit https://maniaurabyrusa.com/",
        from_="+19295436368",
        to="+16465191763",
        )

    print(new_key)

    return redirect('/')

@app.route('/message', methods=['POST'])
@validate_twilio_request
def incoming_message():
    resp = MessagingResponse()

    body = "Лиза, я тебя люблю!" 
    resp.message(body)
    print(request.values['From'])
    print(request.values['Body'])
    return str(resp)

@app.route("/")
def home():
    today = datetime.datetime.now()
    try:
        slots_db_v2 = Slot.query.filter(Slot.opened == True).all()
    except Exception as er:
        print("##/")
        print(er)
        return render_template("apology.html", error_message="Something went wrong.")
    else:
        slots_for_frontend_db_v2 = []
        for slot in slots_db_v2:
            year = slot.date.year
            month = slot.date.month
            day = slot.date.day
            hour = slot.time.hour
            minute = slot.time.minute
            is_open = 1 if slot.opened else 0
            slots_for_frontend_db_v2.append([slot.id, year, month, day, hour, minute, is_open])
        return render_template("index.html", slots=slots_for_frontend_db_v2)

@app.route("/about/")
def about():    
    return render_template("about.html")

@app.route("/account/", methods=["GET", "POST"])
@login_required
def _account():
    return account.account()

@app.route("/add_service/", methods=["GET", "POST"])
def _add_service():
    with app.app_context():
        return add_service.add_service()

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
    with app.app_context():
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

@app.route("/confirm-phone/", methods = ["POST"])
def _confirm_phone():
    
    if request.method == "POST":
        try:                  
            form_data = request.form.to_dict()
            code = request.form.get("code")
            appointment_id = request.form.get("appointment_id")
                    
        except Exception as er:
            print("##/confirm-phone/ --request.form.get")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong") 
    print(code, appointment_id)
    return redirect("/")


@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/day/")
@login_required
def day():
    return render_template("day.html")

@app.route("/delete_service/", methods=["POST", "GET"])
def _delete_service():
    with app.app_context():
        return delete_service.delete_service()


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

@app.route("/edit_service/", methods=["POST", "GET"])
def _edit_service():
    with app.app_context():
        return edit_service.edit_service()

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
        # try:
        token = request.form.get("g-recaptcha-response")
        login = request.form.get("login")
        password = request.form.get("password")
        remember = False if request.form.get("remember") == None else True

        if not validate_recaptcha(token):
            return  render_template("apology.html", error_message="Sorry. Something went wrong with anti robot protection. Please, try again or contact us.")
        
        user_to_login = db_base.session.scalar(select(User).where(User.email == login))
        if user_to_login is None:
            return render_template("apology.html", error_message="wrong login or password user_to_login")
        
        password_ok = verify_and_update_password(password, user_to_login)
        db_base.session.commit()
        if password_ok:

            login_user(user_to_login, remember, "password")
            session["user_id"] = user_to_login.__dict__["id"]
            session["is_admin"] = 1 if user_to_login.has_role("admin") else 0            
            session["name"] = user_to_login.__dict__["name"]
            session["login"] = user_to_login.__dict__["email"]
            session["instagram"] = user_to_login.__dict__["instagram"]
            session["tell"] = user_to_login.__dict__["us_phone_number"]
            return redirect("/")
        else:
            return render_template("apology.html", error_message="wrong login or password password_ok")                

           

    else:
        return render_template("signin.html")
    

@app.route("/signup/", methods = ["GET", "POST"])
@not_loged_only
def _signup():
    return signup.signup()
    
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    log_user_out()
    return redirect("/")

@app.route("/windows/", methods = ["GET", "POST"])
@login_required
@admin_only
def windows():
    db_v2_slots = Slot.query.filter().all()
    slots_to_frontend = []
    for s in db_v2_slots:
        slots_to_frontend.append([s.id, s.date.year, s.date.month, s.date.day, s.time.hour, s.time.minute, 1 if s.opened else 0, 1 if s.occupied else 0])

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
        
@click.command("seed_slots")
@with_appcontext
def seed_slots():
    amount_days = int(os.environ.get("HOW_FAR_IN_FUTURE_CREATE_SLOTS")) if os.environ.get("HOW_FAR_IN_FUTURE_CREATE_SLOTS") else 300
    Slot.create_n_days_upfront(amount_days)
app.cli.add_command(seed_slots)

@click.command("delete_empty_slots")
@with_appcontext
def delete_empty_slots():
    Slot.delete_old_empty()
app.cli.add_command(delete_empty_slots)

@click.command("seed_role")
@with_appcontext
def seed_role():
    role_admin = user_datastore.find_or_create_role("admin")
    role_client = user_datastore.find_or_create_role("client")
    role_tester = user_datastore.find_or_create_role("tester")
    roles = [role_admin, role_client, role_tester]
    db_base.session.add_all(roles)
    db_base.session.commit()

app.cli.add_command(seed_role)


@click.command("seed_admin")
@with_appcontext
def seed_admin():
    if db_base.session.scalar(select(User).where(User.id == 1)) is None:
        admin_email = os.environ.get('ADMINISTRATOR_EMAIL')
        admin_password = os.environ.get('ADMINISTRATOR_PASSWORD')
        admin_name = os.environ.get('ADMINISTRATOR_NAME')
        admin_phone = os.environ.get('ADMINISTRATOR_US_PHONE')
        admin = user_datastore.create_user(
            email = admin_email, 
            password = hash_password(admin_password), 
            name = admin_name, 
            tel = admin_phone, 
            us_phone_number = admin_phone
            )
        db_base.session.add(admin)
        db_base.session.commit()

        user_datastore.add_role_to_user(admin, "admin")
        db_base.session.commit()
        print("created: ", db_base.session.scalar(select(User).where(User.id == 1)))
    else:
        print("already exist: ", db_base.session.scalar(select(User).where(User.id == 1)))
    
app.cli.add_command(seed_admin)

@click.command("seed_test_user")
@with_appcontext
def seed_test_user():
    if db_base.session.scalar(select(User).where(User.id == 2)) is None:
        test_user_email = os.environ.get('TEST_USER_EMAIL')
        test_user_password = os.environ.get('TEST_USER_PASSWORD')
        test_user_name = os.environ.get('TEST_USER_NAME')
        test_user_phone = os.environ.get('TEST_USER_US_PHONE')
        test_user = user_datastore.create_user(
            email = test_user_email, 
            password = hash_password(test_user_password), 
            name = test_user_name, 
            tel = test_user_phone, 
            us_phone_number = test_user_phone
            )
        db_base.session.add(test_user)
        db_base.session.commit()

        user_datastore.add_role_to_user(test_user, "tester")
        db_base.session.commit()
        print("created: ", db_base.session.scalar(select(User).where(User.id == 2)))
    else:
        print("already exist: ", db_base.session.scalar(select(User).where(User.id == 2)))
app.cli.add_command(seed_test_user)

