from flask import redirect, render_template, session
from functools import wraps

def log_user_in(username, password):
    # Query database for username
    #rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    # Ensure username exists and password is correct
    #if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
        #return apology("invalid username and/or password", 403)

    # Remember which user has logged in
    session["user_id"] = username #rows[0]["id"]

    # Redirect user to home page
    return redirect("/")

def log_user_out():
    session["user_id"] = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signin")
        return f(*args, **kwargs)

    return decorated_function

