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
* ```login``` - email, string 
* ```db_cursor``` - cursor of connected database. So before using this function a connection to database should be set, [Cursor](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor) object.
The function returns count of ```login``` in database: 1 or 0.
Query:
```
"SELECT COUNT (id) FROM users WHERE email=?;", (login,)
```
    

### get_service_name(is_manicure, is_pedicure):
It returns service name, that is one of the following strings: ```combo```, ```manicure``` or ```pedicure```
It gets two parameters:
* ```is_manicure``` - 1 or 0, int
* ```is_pedicure``` - 1 or 0, int
This values can be found in database table ```appointments``` 

### log_user_in(login, password, cursor):
It checks username and password (hash), logs user in if ok, returns ```True``` if ok, returns ```False``` if login or password are not correct
It gets 3 parameters:
* ```login``` - email, string
* ```password``` - password, string
* ```cursor``` - cursor of connected database. So before using this function a connection to database should be set, [Cursor](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor) object.
When logs user in the following session values are set:
```
        session["user_id"]
        session["is_admin"]
        session["is_editor"]
        session["name"]
        session["login"]
        session["lang"]
        session["instagram"]
        session["tell"]
        session["is_subscribed"]
        session["avatar"]
```
As long as [Flask-Session](https://flask-session.readthedocs.io/en/latest/) extension for Flask is used in the app the Session is Server-side. 
The data that is required to be saved in the Session is stored in a temporary directory on the server.

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

