import sqlite3
import re

from flask import flash, redirect, render_template, request, session
from ..helpers import validate_recaptcha, validate_password, does_user_exist, log_user_in
from werkzeug.security import  generate_password_hash

def signup():

    try:
        if request.method == "POST":
            token = request.form.get("g-recaptcha-response")
            instagram = request.form.get("instagram")
            tel_number = request.form.get("tel_number")
            login = request.form.get("login")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            if not validate_recaptcha(token):
                return  render_template("apology.html", error_message="Sorry. Something went wrong with anti robot, maybe reCaptcha that you have just checked expired. Please, try arain.")

            is_pass_ok = (password == confirmation) and validate_password(password)
            is_instagram_ok = len(instagram) >= 3
            is_tel_ok = len(tel_number) >= 10
            regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            is_login_ok = (re.fullmatch(regex_email, login) != None)

            if not is_pass_ok or not is_instagram_ok or not is_tel_ok or not is_login_ok:
                return render_template("apology.html", error_message='''
                                       Password must contain:</br>
                                       - a lowercase letter</br>
                                       - a capital (uppercase) letter</br>
                                       - a number</br>
                                       - minimum 6 characters.</br>
                                       </br>
                                       Instagramm name should be valid.</br>
                                        </br>
                                       Telephone at leats 10 digits.</br>
                                        </br>
                                       Email adress.</br>
                                       ''')
        else:
            return render_template("signup.html")
    except Exception as er:
        print("### ERROR signup: request.form, validation")
        print(er)
        return render_template("apology.html", error_message="Something went wrong.")
    else:   
        try:       
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            if does_user_exist(login, cur):            
                error_message = "Email " + login + " already registred, try restore password instead."
                con.close()
                return render_template("apology.html", error_message=error_message)
            #insert new user to db
            cur.execute("INSERT INTO users (is_admin, is_clerck, email, lang, instagram, tel, is_subscribed_promo) values (?, ?, ?, ?, ?, ?, ?)", (0, 0, login, "en", instagram, tel_number, 1))
            user_id = cur.execute("SELECT id FROM users WHERE email=?", (login,)).fetchone()[0]
            password_hash = generate_password_hash(password)
            cur.execute("INSERT INTO login (user_id, hash) VALUES (?, ?)", (user_id, password_hash))
        except Exception as er:
            print("###/signup/ --insert new user to db")
            print(er)
            con.close()
            return render_template("apology.html", error_message="Something went wrong. Try again or contact us.") 
        else:
            log_user_in(login, password, cur)
            con.commit()
            con.close()            
            return redirect("/")