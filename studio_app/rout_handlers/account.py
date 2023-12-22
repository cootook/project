import re
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

def account():
    print("#is admin")
    print(session.get("is_admin"))
    if session.get("is_admit") == 1:
        user_id = request.args.get("user")
        print("#id")
        print(user_id)
    else:
        print("#else")
        user_id = None
    try:
        con = sqlite3.connect("./db.db")
        cur = con.cursor()
        # users (id INTEGER PRIMARY KEY, is_admin INT, is_clerck INT ,  name TEXT, email TEXT, lang TEXT, instagram TEXT, tel TEXT, is_subscribed_promo INT, avatar TEXT);
        user = list(cur.execute("SELECT name, email, lang, instagram, tel, is_subscribed_promo, avatar, is_admin FROM users WHERE id=?", (session.get("user_id") if user_id is None else id, )).fetchone())
        for index in range(len(user)):
            user[index] = "-" if user[index] == None else user[index]

    except Exception as er:
        con.close()
        print("##/account/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
    
    if request.method == "POST":
        try:
            new_name = request.form.get("client_name")
            new_username = request.form.get("username")
            new_tel = request.form.get("tel")
            new_subscribe = 1 if request.form.get("subscribtion") == "on" else 0
            new_email_notify = 1 if request.form.get("notification") == "on" else 0

            print(new_name, new_username, new_tel, new_subscribe, new_email_notify)

            inst_name_regexp=re.compile(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$')
            if inst_name_regexp.match(new_username) is None:
                con.close()
                return render_template("apology.html", error_message="Something went wrong with instagram username.")
            if new_name is None or new_name == "":
                con.close()
                return render_template("apology.html", error_message="Something went wrong with new name.")
            if new_tel is None or new_name == "":
                con.close()
                return render_template("apology.html", error_message="Something went wrong with new telephone number.")


            cur.execute("UPDATE users SET name=?, instagram=?, tel=?, is_subscribed_promo=?", (new_name if not new_name == "-" else None, new_username, new_tel, new_subscribe))
            con.commit()
            return redirect("/account/")
        except Exception as er:
            print("##/account/ --edit")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")
        
    con.close()
    return render_template("account.html", user=user)
