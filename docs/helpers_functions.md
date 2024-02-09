# **helpers.py**

## **Decorators** 

### admin_only:
```admin_only``` goes before route handler function and prevent access for users that are not administrators, redirects to home page if not admin tries to view the route.
    
### login_required:
```login_required``` goes before route handler function and prevent access of not logged in visitors to the route, redirects to ```/signin``` if not logged in.

### not_loged_only(f):
```not_loged_only``` goes before route handler and prevents access of logged in users to the route, redirects to home page if logged in

## **Functions**

### does_user_exist(login, db_cursor):
```does_user_exist``` checks if ```login``` (email) is in database, gets two parameters:
* ```login``` - email 
* ```db_cursor``` - cursor of connected database. So before using this function a connection to database should be set.
The function returns count of ```login``` in database: 1 or 0.
Query:
```
"SELECT COUNT (id) FROM users WHERE email=?;", (login,)
```
    

### get_service_name(is_manicure, is_pedicure):
    servise_name = ""
    if is_manicure == 1 and is_pedicure == 1:
        servise_name = "combo"
    elif is_manicure == 1 and not is_pedicure == 1:
        servise_name = "manicure"
    else:
        servise_name = "pedicure"
    return servise_name

### log_user_in(login, password, cursor):
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
        # id, is_admin INT, is_editor INT, name TEXT, email TEXT, lang TEXT, instagram TEXT, tel TEXT, is_subscribed_promo INT, is_instagram_notification INT, is_email_notification INT, is_text_notification INT, avatar TEXT
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
    # Redirect user to home page
    # return redirect("/")

### log_user_out():
    session["user_id"] = None





### page_not_found(e):
  error_message  = "404 - page not fond"
  return render_template('apology.html', error_message = error_message), 404

### validate_recaptcha (token):
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

### validate_password (password):
    is_lower = re.search("[a-z]", password) != None
    is_capital = re.search("[A-Z]", password) != None
    is_number = re.search("[0-9]", password) != None
    is_length = len(password) >= 6
    if is_lower and is_capital and is_number and is_length:
        return True
    else:
        return False

