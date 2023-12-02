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
* register via login/password or facebook 
* login/logout from user account via facebook
* user can see the history of it's appointments
* admin can open and close time for booking
* admin can manage appointments
###    
**future features:**
* HTTPS
* reCAPTCHA
* language selection 
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
* Users (id, is_admin, is_clerck, instagram_name, email, lang, tel, is_subscribed_promo, avatar)
* Login (user_id, hash, fb, google)
* Calendar(slot_id, year, month, weekday, day, hour, minute, is_open)
* Appointments (id, user_id, service_name, slot_id, is_seen, is_aproved)
* Sessions (user_id, from, to,  year, month, day, hour, minute, second, data)
