import sqlite3
import datetime

from flask import render_template, request, session
from ..helpers import validate_password, log_user_in
from werkzeug.security import  generate_password_hash

def change_password():    
    if request.method == "POST":
        today = datetime.datetime.now()
        try:
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirmation = request.form.get("new_confirmation")

            if not log_user_in(session.get("login"), current_password, cur):
                return render_template("apology.html", error_message="Wrong current password!.")

            is_new_pass_ok = (new_password == confirmation) and validate_password(new_password)
            
            if not is_new_pass_ok:
                return render_template("apology.html", error_message='''
                                        
                                        Password must contain:</br>
                                        - a lowercase letter</br>
                                        - a capital (uppercase) letter</br>
                                        - a number</br>
                                        - minimum 6 characters.</br>
                                        
                                        ''')
            
            password_hash = generate_password_hash(new_password)
            cur.execute("UPDATE login SET hash=? WHERE user_id=?", (password_hash, session.get("user_id")))
            con.commit()
            
            if not log_user_in(session.get("login"), new_password, cur):
                print("### password NOT changed", session.get("user_id"))
                con.close()
                return render_template("apology.html", error_message="Something went wrong. Try again or contact administrator if it is not working.")
            else:
                print("### password changed", session.get("user_id"))
                con.close()
                return render_template("message_page.html", message_title="Password changed", 
                                                            message_header="Success!", 
                                                            message_text="Password chanded.", 
                                                            message_link="/", 
                                                            message_link_text="Home page.")
        except Exception as er:
            print("### ERROR change_password: request.form, validation, db")
            print(er)
            con.close()
            return render_template("apology.html", error_message="Something went wrong.")
    else:
        return render_template("change_password.html")
