import datetime
import sqlite3
import os

from flask import redirect, render_template, request, session
from studio_app.helpers import get_service_name
from ..helpers import validate_recaptcha

def change_role():
    today = datetime.datetime.now()
    
    if request.method == "POST":
        # user_id: 1
        # action: make_admin
        # key: d
        # g-recaptcha-response:
        try:
            user_id_set_role = request.form.get("user_id")
            user_commiting_change = session.get("user_id")
            action = request.form.get("action")
            recaptcha_response = request.form.get("g-recaptcha-response")
            key_for_change = request.form.get("key")
            if (key_for_change != os.environ.get('KEY_CHANGE_ROLE')): 
                return  render_template("apology.html", error_message="Access denied: key")
            elif (not validate_recaptcha(recaptcha_response)):
                return  render_template("apology.html", error_message="Access denied: recaptcha")
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            if action == "make_admin":
                cur.execute("UPDATE users SET is_admin=1 WHERE id=?", (user_id_set_role,))
            elif action == "discard_admin":
                cur.execute("UPDATE users SET is_admin=0 WHERE id=?", (user_id_set_role,))                
            elif action == "meke_editor":
                cur.execute("UPDATE users SET is_editor=1 WHERE id=?", (user_id_set_role,))
            elif action == "discard_editor":
                cur.execute("UPDATE users SET is_editor=0 WHERE id=?", (user_id_set_role,))
            else:
                return  render_template("apology.html", error_message="wrong action")
                
            cur.execute('''INSERT INTO sessions 
                        (
                            user_id, 
                            from_route, 
                            to_route, 
                            year, 
                            month, 
                            day, 
                            hour, 
                            minute, 
                            second, 
                            type, 
                            data
                        ) 
                        VALUES 
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', 
                        (
                            user_commiting_change,
                            "/change_role/?key=",
                            "/change_role/",
                            today.year,
                            today.month,
                            today.day,
                            today.hour,
                            today.minute,
                            today.second,
                            "db",
                            f"action: {action}, for: {user_id_set_role}"
                        )
                        )    
            con.commit()
            con.close()
            return redirect("/change_role/?key=" + os.environ.get('KEY_CHANGE_ROLE_LIST'))

        except Exception as er:
            con.close()
            print("##/change_role/ --POST")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")
        
    else:        
        try:
            key = request.args.get("key")
            if key != os.environ.get('KEY_CHANGE_ROLE_LIST'):
                print("### Access denied!: ", key, today, session.get("user_id"))
                return  render_template("apology.html", error_message="Access denied!") 
               
            print("#change role: ", key, today, session.get("user_id"))    
            
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            
            clients_db = cur.execute("SELECT id, name, instagram, is_admin, is_editor, id FROM users").fetchall()
            clients = list()
            for client in clients_db:
                temp_client_dict = {}
                temp_client_dict["id"] = client[0]
                temp_client_dict["name"] = "-" if client[1] == None else client[1]
                temp_client_dict["instagram"] = client[2]
                temp_client_dict["is_admin"] = client[3]
                temp_client_dict["is_editor"] = client[4]

                clients.append(temp_client_dict) 
            print(clients)
            con.close()
            print(key)
            return render_template("change_role.html", clients=clients)
        
        except Exception as er:
            con.close()
            print("##/change_role/ --GET")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")
        
