##
# **development in progress**
##
# nail studio booking
#### web app
###
This is a final project of **[Harvard CS50](https://pll.harvard.edu/course/cs50-introduction-computer-science)** course. 
Web app for booking maniqure appointments and managing them.
###
**Using:**
* flask (jinja)
* bootstrap
* SQLite
* Flask-Session
* werkzeug.security
###
**planing canges (to do list):**
* make it possible to edit appointments
* add more settings of notification to user table of db
* make it possible to delete account forever
* add pic to user profile
* add list of time slots that are occupide by appointment to db
* remake appointments as tiles (not table)
* make it possible to edit windows (open/close time slots) withot refreshing page (stay on the same element after editing)
* refactor: split webapp.py into multiple files with only function included
* add atempt limit to login table in db
**features:**
* optimized for small screens
* session uses filesystem (instead of signed cookies)
* register via login/password 
* login/logout from user account
* user can see the history of appointments
* admin can open and close time for booking
* admin can manage appointments
* admin can edit user profile
###    
**future features:**
* email notification and confirmation
* HTTPS
* write logs into db
* testing (QI)
* stat and metrics (google?)
* reCAPTCHA
* language selection 
* sign up with Facebook
* sign up with Google
* instagram bot
* get rid of moment.js
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
* CREATE TABLE appointments (id INTEGER PRIMARY KEY, user_id INT, pedicure INT, manicure INT, message TEXT, slot_id INT, amount_time_min INT, slots_in TEXT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id)); 
* CREATE TABLE sessions (rowid INTEGER PRIMARY KEY, user_id INT, from_route TEXT, to_route TEXT,  year INT, month INT, day INT, hour INT, minute INT, second INT, type TEXT, data TEXT, FOREIGN KEY (user_id) REFERENCES users(id));
