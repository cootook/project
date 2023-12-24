import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

def book():
    if request.method == "POST":
        try:
            minute = int(request.form.get("minute"))
            hour = int(request.form.get("hour"))
            day = int(request.form.get("date"))
            month = int(request.form.get("month")) + 1 # in calendar.js month range starts from 0
            year = int(request.form.get("year"))
            #calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT);
            #appointments (id INTEGER PRIMARY KEY, user_id INT, service_name TEXT, slot_id INT, amount_time_min INT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id));
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            slot_to_book = cur.execute("SELECT slot_id, is_open FROM calendar WHERE year=? AND month=? AND day=? AND hour=? AND minute=?;", (year, month, day, hour, minute)).fetchone()
            is_open = True if slot_to_book[1] == 0 else False
            slot_id = slot_to_book[0]
            cur.execute("UPDATE calendar SET is_open=0 WHERE slot_id=?;", (slot_id,))
            cur.execute("INSERT INTO appointments (user_id, slot_id, is_seen, is_aproved, is_canceled, amount_time_min) VALUES (?, ?, 0, 0, 0, 120);", (session.get("user_id"), slot_id))
            con.commit()
            con.close()
            return redirect("/")
        
        except Exception as er:
            con.close()
            print("##/book/ --request.form.get, db query")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")        

    else:
        return redirect("/")
