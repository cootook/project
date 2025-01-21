# booking app for manicure salon in New York City
**[ManiAuraByRusa.com](https://www.maniaurabyrusa.com/)**

## migrations and seed

if there is no 'migrations' directory : run 
    ```console
        flask bb init
    ```
    to file 'migrations/script.py.mako' add imports
    ```python
        import flask_security
        from flask_security.models import fsqla_v3 as fsqla
        from typing import Optional
    ```
else:
    make sure imports were added

run
```console
    flask db migrate
```
migration should be ran on each models mutations 

check auto created scripts in 'migrations/versions', first of all imports
if there is any data in database make sure that new fields are not 'nullable = False', because in old lines these fields are going to be set 'null'

```console
    flask db upgrade
```

before seeding any user seed roles

```console
    flask seed_role
```

ADMIN settings in '.env' (terminal reload for changes to apply) 

```console
    flask seed_admin
```

TEST_USER settings in '.env' (terminal reload for changes to apply)

```console
    flask seed_test_user
```

default days upfront for creating slots is 300 days, change in '.env' (terminal reload for changes to apply)

```console
    flask seed_slots
```




How it works while contributing this project? Like that:
* learn ```something```
* write a ticket with comprehensive explanation about a thing that should be build with ```something```
* build the thing with ```something``` 
* get a review and ideas about builded thing
* try to find best practices or alternatives
* rebuild or upgrade the thing
* write docs about the thing
* create pull request 
* get reviews 
* become a star))

 *correct these steps or add something*


Everybody welcome!

If you are going to participate we assume you are accepting [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](/CODE_OF_CONDUCT.md) .

Also take a look at [Contributing.md](/CONTRIBUTING.md) to get info about how to participate.

### we create a booking app

#### Description: 
Web app to manage appointments, client's info, content. Current version is for manicure or pedicure in nail studio of one nail technician. In the future we are going to make it editable via admin panel. So the app can be adapted for any purpose.

![home page](/docs/images/calendar.png)

#### What the app has now:
Each client has an account.

![creating account](/docs/images/signup.png)

![creating account](/docs/images/signup_filled.png)

![account](/docs/images/account.png)

Clients can book or cancel appointments and edit their information (name, telephone, etc.). 

![request for an appointment](/docs/images/request.png)

![appointment](/docs/images/appointment.png)

Administrators can confirm, edit, cancel, or mark appointments as done. They can also edit client information and manage available time in the calendar by adding or removing slots.

![make admin](/docs/images/make_admin.png)

![windows](/docs/images/windows.png)

![admin view of appointments](/docs/images/apointment_admin_view.png)

#### What would be good to add:
* content management system for editing articles
* add some alternative calendars, timelines
* admin panel to adjust the app for any needs, set admins and editors
* scale app for two or more workers 
* bots for social media for notifications 
* paying methods

### **Technologies:**

#### **backend**:
* Python - Flask (jinja)
* SQLite

#### **frontend**
* bootstrap
* jQuery (for Bootstrap only)
* vanilla JavaScript 

#### **some plans:**
* get rid of jQuery and moment.js
* use Flask Security Too for password dealing
* rebuild backend with Django, Node.JS, GO
* rebuild frontend with React
* deploy project

#### **features:**
* optimized for small screens (bootstrap)
* register via login/password 
* login/logout from user account
* change password
* setting user as admin via web app
* user can see the history of appointments
* admin can open and close time for booking
* admin can manage appointments
* admin can edit user profile
* protected from bots with Google reCAPTCHA
* email sender (Python mail)

#### **future features:**
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
* create Android app
* create iOS app

### **Documentations**
* rules of the community: [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](/CODE_OF_CONDUCT.md)
* guide how to participate: [Contributing.md](/CONTRIBUTING.md)
* how to write commit message: [commit](/docs/commit_message_format.md)
* app functions docs: [helpers](/docs/helpers_functions.md), [route_handlers](/docs/route_handlers.md)
* license MIT: [LICENSE](/LICENSE)

##### This project is not deployed yet. 

```
project
├─ .gitignore
├─ CODE_OF_CONDUCT.md
├─ CONTRIBUTING.md
├─ docs
│  ├─ commit_message_format.md
│  ├─ database_schema.md
│  ├─ files
│  ├─ helpers_functions.md
│  ├─ images
│  │  ├─ account.png
│  │  ├─ apointment_admin_view.png
│  │  ├─ appointment.png
│  │  ├─ calendar.png
│  │  ├─ db_schema.png
│  │  ├─ make_admin.png
│  │  ├─ request.png
│  │  ├─ signup.png
│  │  ├─ signup_filled.png
│  │  └─ windows.png
│  ├─ pull_request_template.md
│  └─ route_handlers.md
├─ env_config_info.txt
├─ LICENSE
├─ migrations
│  ├─ alembic.ini
│  ├─ env.py
│  ├─ README
│  ├─ script.py.mako
│  └─ versions
│     ├─ 11b4045c2dcb_.py
│     └─ a0e6bbf34d48_.py
├─ README.md
├─ requirements.txt
└─ studio_app
   ├─ config.py
   ├─ db_classes.py
   ├─ f2c5930a29900498068d74013e18e78c.html
   ├─ forms.py
   ├─ helpers
   │  ├─ email.py
   │  ├─ phone.py
   │  ├─ recaptcha.py
   │  ├─ sms.py
   │  └─ __init__.py
   ├─ helpers_legacy.py
   ├─ rout_handlers
   │  ├─ account.py
   │  ├─ add_service.py
   │  ├─ all_appointments.py
   │  ├─ all_history.py
   │  ├─ appointments.py
   │  ├─ book.py
   │  ├─ cancel_appointment.py
   │  ├─ change_password.py
   │  ├─ change_role.py
   │  ├─ confirm_appointment.py
   │  ├─ confirm_phone.py
   │  ├─ delete_service.py
   │  ├─ done_appointment.py
   │  ├─ edit_appointment.py
   │  ├─ edit_service.py
   │  ├─ history.py
   │  ├─ signup.py
   │  └─ __init__.py
   ├─ services
   │  ├─ booking.py
   │  ├─ user.py
   │  └─ verification.py
   ├─ static
   │  ├─ css
   │  │  ├─ account.css
   │  │  ├─ all_appointments.css
   │  │  ├─ bootstrap.min.css
   │  │  ├─ bootstrap.min.css.map
   │  │  ├─ calendar.css
   │  │  ├─ clients.css
   │  │  ├─ contact.css
   │  │  ├─ form-validation.css
   │  │  ├─ header_navbar.css
   │  │  ├─ layout.css
   │  │  └─ style.css
   │  ├─ img
   │  │  └─ icon.svg
   │  └─ js
   │     ├─ account.js
   │     ├─ all_appointments.js
   │     ├─ booking_sms_confirmation_code.js
   │     ├─ bootstrap.bundle.min.js
   │     ├─ bootstrap.bundle.min.js.map
   │     ├─ calendar.js
   │     ├─ change_password.js
   │     ├─ form-validation.js
   │     ├─ index.js
   │     ├─ moment.js
   │     ├─ signin.js
   │     └─ signup.js
   ├─ templates
   │  ├─ about.html
   │  ├─ account.html
   │  ├─ add_service.html
   │  ├─ all_appointments.html
   │  ├─ all_history.html
   │  ├─ apology.html
   │  ├─ appointments.html
   │  ├─ appointment_request.html
   │  ├─ articles.html
   │  ├─ booking_sms_confirmation_code.html
   │  ├─ calendar.html
   │  ├─ change_password.html
   │  ├─ change_role.html
   │  ├─ clients.html
   │  ├─ contact.html
   │  ├─ day.html
   │  ├─ delete_service.html
   │  ├─ edit_service.html
   │  ├─ header_navbar.html
   │  ├─ history.html
   │  ├─ index.html
   │  ├─ layout.html
   │  ├─ message_page.html
   │  ├─ pricing.html
   │  ├─ privacy_policy.html
   │  ├─ security
   │  │  ├─ login_user.html
   │  │  ├─ register_user.html
   │  │  ├─ _macros.html
   │  │  └─ _menu.html
   │  ├─ signin.html
   │  ├─ signup.html
   │  ├─ terms_of_service.html
   │  └─ windows.html
   └─ webapp.py

```