##
# **development in progress**
##
# nail studio booking
#### web app
###
This is a final project of **Harvard CS50** course. 
Web app for booking maniqure appointments and managing them.
###
**Using:**
* flask
* bootstrap
* SQLite
* Flask-Session
* werkzeug.security
###
**features:**
* optimized for small screens
* session uses filesystem (instead of signed cookies)
* register via login/password 
* login/logout from user account
* user can see the history of it's appointments
* admin can open and close time for booking
* admin can manage appointments
###    
**future features:**
* email notification and confirmation
* HTTPS
* reCAPTCHA
* language selection 
* sign up with Facebook
* sign up with Google
* instagram bot
* admin can add articles
* add user *clerk* to manage *articles* and *about* 
* create Android app
* create iOS app
###
*requirements.txt* contains info about modules and extensions to be installed for this app.
#####
*.env* for setting enviroment variables to switch prodaction/development and debug on/off
#####
set user as admin  in *db.db* manualy *users.is admin = 1*
#####
### Database structure
* CREATE TABLE users (id INTEGER PRIMARY KEY, is_admin INT, is_clerck INT ,  name TEXT, email TEXT, lang TEXT, instagram TEXT, tel TEXT, is_subscribed_promo INT, avatar TEXT);
* CREATE TABLE login (user_id INTEGER PRIMARY KEY, hash TEXT, fb TEXT, google TEXT, FOREIGN KEY(user_id) REFERENCES users(id));
* CREATE TABLE calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT);
* CREATE TABLE appointments (id INTEGER PRIMARY KEY, user_id INT, service_name TEXT, slot_id INT, amount_time_min INT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id));
* CREATE TABLE sessions (rowid INTEGER PRIMARY KEY, user_id INT, from_route TEXT, to_route TEXT,  year INT, month INT, day INT, hour INT, minute INT, second INT, type TEXT, data TEXT, FOREIGN KEY (user_id) REFERENCES users(id));
