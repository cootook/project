## hello there!

This is a learning project, so any contributors are welcome

It would be great if you share some knowledge and experience.
Feel free to expose your ideas.
If you are experienced dev please show the right direction for our efforts, roast our mistakes.

[Here](https://github.com/users/cootook/projects/1/views/1) is kanban for this project.
You can pick up something or make a review. Also you can add something via [issues](https://github.com/cootook/project/issues) using templates.

## get started
### workflow
We work with the app via issues (tickets). Any feature, bug, refactor, rebuilding, docs editing requires to be exposed in a new issue with good explanation. There are templates for issues and PR (pull request). It is ok to communicate via issues by creating and editing or using internal chat.
For vast majority of issues (tickets) we create a branch. 
All PR are merging into [dev](https://github.com/cootook/project/tree/dev) branch, after testing [dev](https://github.com/cootook/project/tree/dev) branch merges into [main](https://github.com/cootook/project/tree/main) branch. So [main](https://github.com/cootook/project/tree/main) is the last working version before release. 
When really big changes are made we create a new branch from [main](https://github.com/cootook/project/tree/main) for previous version. 
In my mind [dev](https://github.com/cootook/project/tree/dev) is beta, and [main](https://github.com/cootook/project/tree/main) is a release candidate. Any other branch is OLD VERSION or alfa.
There is no such thing as testing in this project yet. 
### environment
Python should be installed, virtual environment created and activated.

*requirements.txt* contains info about modules and extensions to be installed for this app.
[Install](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#using-a-requirements-file) modules.

Configure *.env* for setting environment variables. File ```.env``` is in ```.gitignore``` so it should be created manually:
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

Create data base file in the root directory, name it "db.db". Or you can copy and rename file [_db.db](/docs/files/_db.db) where all tables exist, also there are two users:
* admin: login ```admin@name.name``` password ```Newuser12345```
* user: login ```admin@name.name``` password ```Newuser12345```

It is SQLite. Python has a [module](https://docs.python.org/3/library/sqlite3.html) for this already. Odds aer we will use SQL Alchemy in the future.
To read database file you can use VScode extension [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer).

### Database schema

```
CREATE TABLE users (
    id INTEGER PRIMARY KEY, 
    is_admin INT, 
    is_editor INT, 
    name TEXT, email TEXT, 
    lang TEXT, instagram TEXT, 
    tel TEXT, 
    is_subscribed_promo INT, 
    is_instagram_notification INT, 
    is_email_notification INT, 
    is_text_notification INT, 
    avatar TEXT);
```

```
CREATE TABLE login (
    user_id INTEGER PRIMARY KEY, 
    hash TEXT, 
    stay_logedin INT, 
    date_registered TEXT, 
    last_login TEXT, 
    count_atempts INT, 
    FOREIGN KEY(user_id) REFERENCES users(id));
```

```
CREATE TABLE calendar (
    slot_id INTEGER PRIMARY KEY, 
    year INT, 
    month INT, 
    day INT, 
    hour INT, 
    minute INT, 
    is_open INT, 
    is_occupaied INT);
```

```
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY, 
    user_id INT, 
    pedicure INT, 
    manicure INT, 
    message TEXT, 
    slot_id INT, 
    amount_time_min INT, 
    is_seen INT, 
    is_aproved INT, 
    is_canceled INT, 
    FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), 
    FOREIGN KEY (user_id) REFERENCES users(id));
``` 

```
CREATE TABLE sessions (
    rowid INTEGER PRIMARY KEY, 
    user_id INT, 
    from_route TEXT, 
    to_route TEXT,  
    year INT, 
    month INT, 
    day INT, 
    hour INT, 
    minute INT, 
    second INT, 
    type TEXT, 
    data TEXT, 
    FOREIGN KEY (user_id) REFERENCES users(id));
```

To change role of any user go to route "/change_role?key=```KEY_CHANGE_ROLE_LIST```". Than hit the button, enter ```KEY_CHANGE_ROLE```, pass reCAPTCHA.


### **ATTENTION**
When you are switching branches ignored by git files can be lost. So keep a copy of them somewhere. If you know how to automate this proses or to do it other way share please.

Do NOT share your private info via .env or db.db Do not use your real existing passwords and telephone numbers for testing.

### while doing
* Please follow [commit guide](/docs/commit_message_format.md) and [pull request template](/docs/pull_request_template.md)
* When creating or changing make sure to write some explanation in [helpers](/docs/helpers_functions.md) or [route handlers](/docs/route_handlers.md)
* If your actions are about database schema or installing new extensions/modules do not forget to update [Contributing](contributing.md) 