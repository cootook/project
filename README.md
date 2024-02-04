# project
```*learn-by-doing*```

That was [@cootook's](https://github.com/cootook) final project of **[Harvard CS50](https://pll.harvard.edu/course/cs50-introduction-computer-science)** course in 2023.
I decided not to throw it away but to use it for my future learning. Now it is a learn-by-doing project. The goal is to bridge the gap between learning code and launching a success career and being promoted.

The main part of that is to create real-world-like project for learners. I believe it is good to invent the wheel before using out of the box solution, it is ok to build the same thing again and again, it is ok to get specific related to the subject critics and advices.
In my mind any programmer job is not about coding only. And coding is not the main part at all. Coder should be able to:
* be a creative problem solver 
* find and fix a cause or a root not an effect
* deny yourself to fix than not broken
* read and understand docs
* write a comprehensive explanations and messages
* follow existing codes and rules 
* read and understand code written by others (self written too)
* constantly to learn new things

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

# project
### create a booking app

#### Description: 
Web app to manage appointments, client's info, content. Current version is for manicure or pedicure in nail studio of one nail technician. In the future we are going to make it editable via admin panel. So the app can be adapted for any purpose.

#### What the app has now:
Each client has an account. Clients can book or cancel appointments and edit their information (name, telephone, etc.). Administrators can confirm, edit, cancel, or mark appointments as done. They can also edit client information and manage available time in the calendar by adding or removing slots.

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

##### **future features:**
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


##### This project is not deployed yet. 