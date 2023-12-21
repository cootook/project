import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

def account():
    try:
        con = sqlite3.connect("./db.db")
        cur = con.cursor()
        # users (id INTEGER PRIMARY KEY, is_admin INT, is_clerck INT ,  name TEXT, email TEXT, lang TEXT, instagram TEXT, tel TEXT, is_subscribed_promo INT, avatar TEXT);
        user = list(cur.execute("SELECT name, email, lang, instagram, tel, is_subscribed_promo, avatar FROM users WHERE id=?", (session.get("user_id"), )).fetchone())
        for index in range(len(user)):
            user[index] = "-" if user[index] == None else user[index]

    except Exception as er:
        con.close()
        print("##/account/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
    return render_template("account.html", user=user)
