import re
from flask import redirect, render_template, session
from werkzeug.security import check_password_hash
from functools import wraps

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("is_admin")==0:
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function


def does_user_exist(login, db_cursor):
    return db_cursor.execute("SELECT COUNT (id) FROM users WHERE email=?;", (login,)).fetchone()[0] == 1

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
        #seve user info 
        session["user_id"] = user_id[0] #rows[0]["id"]
        session["is_admin"] = user[1]
        session["is_clerck"] = user[2]
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
    # Redirect user to home page
    # return redirect("/")

def log_user_out():
    session["user_id"] = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin")
        return f(*args, **kwargs)

    return decorated_function

def not_loged_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def page_not_found(e):
  error_message  = "404 - page not fond"
  return render_template('apology.html', error_message = error_message), 404

def validate_password (password):
    is_lower = re.search("[a-z]", password) != None
    is_capital = re.search("[A-Z]", password) != None
    is_number = re.search("[0-9]", password) != None
    is_length = len(password) >= 6
    if is_lower and is_capital and is_number and is_length:
        return True
    else:
        return False

