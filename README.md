# nail studio booking
#### Description: web app to manage appointments for manicure or pedicure in nail studio.  
#### Each client has an account. Clients can book or cancel appointments and edit their information (name, telephone, etc.). Administrators can confirm, edit, cancel, or mark appointments as done. They can also edit client information and manage available time in the calendar by adding or removing slots.
###
This is a final project of **[Harvard CS50](https://pll.harvard.edu/course/cs50-introduction-computer-science)** course. 
###
**Technologies:**
* flask (jinja)
* flask-security-too
* bootstrap
* jQuery (for Bootstrap only)
* SQLite
* werkzeug.security
* JavaScript 
* google reCAPTCHA
###
**planing canges (to do list):**
take a look at issues (GitHub)
###
**features:**
* optimized for small screens
* session uses filesystem (instead of signed cookies)
* register via login/password 
* login/logout from user account
* user can see the history of appointments
* admin can open and close time for booking
* admin can manage appointments
* admin can edit user profile
* protected from bots
###    
**future features:**
* email notification and confirmation
* HTTPS
* write logs into db
* testing (QI)
* stat and metrics (google?)
* language selection 
* sign up with Facebook
* sign up with Google
* instagram bot
* admin can add articles
* add user *editor* to manage *articles* and *about* 
* create Android app
* create iOS app
###
*requirements.txt* contains info about modules and extensions to be installed for this app.
#####
*.env* for setting enviroment variables:
```
FLASK_APP=studio_app.webapp
FLASK_ENV=development
FLASK_DEBUG=1
MAIL_USERNAME=*
MAIL_APP_KEY=*
MAIL_DEFAULT_SENDER=*
SECRET_KEY=*
SECRET_RECAPTCHA=*
KEY_CHANGE_ROLE_LIST=*
KEY_CHANGE_ROLE=*
```
#####
To change role of any user go to route "/change_role?key=*KEY_CHANGE_ROLE_LIST*". Than hit the button, enter *KEY_CHANGE_ROLE*, pass reCAPTCHA.
#####
### Create data base file in the root directory, name it "db.db"
### Database structure
* ```CREATE TABLE users (id INTEGER PRIMARY KEY, is_admin INT, is_editor INT, name TEXT, email TEXT, lang TEXT, instagram TEXT, tel TEXT, is_subscribed_promo INT, is_instagram_notification INT, is_email_notification INT, is_text_notification INT, avatar TEXT);```
* ```CREATE TABLE login (user_id INTEGER PRIMARY KEY, hash TEXT, stay_logedin INT, date_registered TEXT, last_login TEXT, count_atempts INT, FOREIGN KEY(user_id) REFERENCES users(id));```
* ```CREATE TABLE calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, day INT, hour INT, minute INT, is_open INT, is_occupaied INT);```
* ```CREATE TABLE appointments (id INTEGER PRIMARY KEY, user_id INT, pedicure INT, manicure INT, message TEXT, slot_id INT, amount_time_min INT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id));``` 
* ```CREATE TABLE sessions (rowid INTEGER PRIMARY KEY, user_id INT, from_route TEXT, to_route TEXT,  year INT, month INT, day INT, hour INT, minute INT, second INT, type TEXT, data TEXT, FOREIGN KEY (user_id) REFERENCES users(id));```
