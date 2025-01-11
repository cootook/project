import datetime
import os
import re
import requests
import smtplib
import json
import phonenumbers

from flask import redirect, render_template, session, abort, current_app, request
from werkzeug.security import check_password_hash
from functools import wraps
from twilio.request_validator import RequestValidator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("is_admin")==0:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function


def does_user_exist(login, db_cursor):
    return db_cursor.execute("SELECT COUNT (id) FROM users WHERE email=?;", (login,)).fetchone()[0] == 1

def get_js_object(object):
    def convert(obj):
        for el in obj:
            if isinstance(obj[el], datetime.datetime):
                obj.update({el: obj[el].strftime('%Y-%m-%dT%H:%M:%S')})
            elif isinstance(obj[el], datetime.date):
                obj.update({el: obj[el].strftime("%m/%d/%Y")})
            elif isinstance(obj[el], datetime.time):
                obj.update({el: obj[el].strftime("%H:%M")})
        return obj
    
    if isinstance(object, list):        
        for element in object:
            element = convert(element)
    else:
        object = convert(object)
        
    return json.dumps(object)

def get_service_name(is_manicure, is_pedicure):
    servise_name = ""
    if is_manicure == 1 and is_pedicure == 1:
        servise_name = "combo"
    elif is_manicure == 1 and not is_pedicure == 1:
        servise_name = "manicure"
    else:
        servise_name = "pedicure"
    return servise_name

def log_user_in(login, password, cursor):
    # Query database for username
    if not does_user_exist(login, cursor):
        return False
    #rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    # Ensure username exists and password is correct
    #if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
        #return apology("invalid username and/or password", 403)
    try:
        user_id = cursor.execute("SELECT id FROM users WHERE email=?", (login,)).fetchone()#[0]
    except Exception as er:
        print("### ERROR select from user")
        print(er)
    
    try:
        hash_from_db = cursor.execute("SELECT hash FROM login WHERE user_id=?", (user_id)).fetchone()[0]
    except Exception as er:
        print("### ERROR select from login")
        print(er)

    try: 
        is_password_correct = check_password_hash(hash_from_db, password)
    except Exception as er:
        print("### ERROR check_password_hash")
        print(er)

    if is_password_correct:
        user = cursor.execute("SELECT * FROM users WHERE email=?", (login,)).fetchone()
        session["user_id"] = user_id[0] 
        session["is_admin"] = user[1]
        session["is_editor"] = user[2]
        session["name"] = user[3]
        session["login"] = login
        session["lang"] = user[5]
        session["instagram"] = user[6]
        session["tell"] = user[7]
        session["is_subscribed"] = user[8]
        session["avatar"] = user[9]
        return True
    else:
        return False

def log_user_out():
    session["user_id"] = None
    session.clear()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin")
        return f(*args, **kwargs)

    return decorated_function

def send_email(to_email: str, subject: str, plain_text, from_email: str = None, from_field_name = ""):
    """
    returns OK or error as str
    
    there is no validations of passed params in that func

    look at .env and config.py to configure
    """
    if from_email is None:
        from_email = os.environ.get('MAIL_DEFAULT_SENDER')
    mail_server = os.environ.get('MAIL_SERVER')
    port = int(os.environ.get('MAIL_PORT'))
    username = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')

    message = MIMEMultipart("alternative")
    message['Subject'] = subject
    message['To'] = to_email
    message['From'] = f"{from_field_name} <{from_email}>"

    text = plain_text

    part1 = MIMEText(text, "plain")

    message.attach(part1)

    try:
        server = smtplib.SMTP(mail_server, port)
        server.starttls()
        server.login(username, password)
        txt = message.as_string()
        server.sendmail(from_email, to_email, txt)
        server.quit()
        return "OK"
    except Exception as error:
        return str(error)
    

def not_loged_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def send_sms(from_number, to_number, sms_body):
    def is_number_valid(number):
        parsed_phone = phonenumbers.parse(number, None)
        is_parsed_number_valid = phonenumbers.is_valid_number(parsed_phone)
        if not is_parsed_number_valid:
            return False
        else:
            return True
    if not is_number_valid(from_number):
        return "INVALID FROM"
    elif not is_number_valid(to_number):
        return "INVALID TO"
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    new_key = client.new_keys.create(friendly_name="test sms")

    message = client.messages.create(
        body=sms_body,
        from_=from_number,
        to=to_number,
        )

    print("# send_sms: ", new_key)

    return "OK"

def page_not_found(e):
  error_message  = "404 - page not fond"
  return render_template('apology.html', error_message = error_message), 404

def validate_recaptcha (token):
    try:
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
        "secret": os.environ.get('SECRET_RECAPTCHA'),
        "response": token
        }

        recaptcha = requests.post(url, params)
        recaptcha_respond_dict = json.loads(recaptcha.text)

        if not recaptcha_respond_dict['success']:
            return False
        else: 
            return True
    except Exception as er:
        print("#helpers.validate_recaptchs ---recaptcha request")
        print(er)
        return  False

def validate_password (password):
    is_lower = re.search("[a-z]", password) != None
    is_capital = re.search("[A-Z]", password) != None
    is_number = re.search("[0-9]", password) != None
    is_length = len(password) >= 6
    if is_lower and is_capital and is_number and is_length:
        return True
    else:
        return False
    
def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))

        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        if request_valid or current_app.debug:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function

