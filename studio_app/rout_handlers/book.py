import sqlite3

from flask import flash, redirect, render_template, request, session
from ..helpers import validate_recaptcha

def book():
    if request.method == "POST":
        try:                  
            token = request.form.get("g-recaptcha-response")
            minute = int(request.form.get("minute"))
            hour = int(request.form.get("hour"))
            day = int(request.form.get("date"))
            month = int(request.form.get("month")) + 1 # in calendar.js month range starts from 0
            year = int(request.form.get("year"))
            manicure = 1 if request.form.get("manicure") is not None else 0
            pedicure = 1 if request.form.get("pedicure") is not None else 0
            message = request.form.get("message-text")

        except Exception as er:
            con.close()
            print("##/book/ --request.form.get")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong") 

        if not validate_recaptcha(token):
            return  render_template("apology.html", error_message="Sorry. Something went wrong with anti robot, maybe reCaptcha that you have just checked expired. Please, try arain.")

        try:            
            #calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT);
            #appointments (id INTEGER PRIMARY KEY, user_id INT, pedicure INT, manicure INT, message TEXT, slot_id INT, amount_time_min INT, slots_in TEXT, is_seen INT, is_aproved INT, is_canceled INT, FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), FOREIGN KEY (user_id) REFERENCES users(id));
            con = sqlite3.connect("./db.db") 
            cur = con.cursor()
            slot_to_book = cur.execute("SELECT slot_id, is_open FROM calendar WHERE year=? AND month=? AND day=? AND hour=? AND minute=?;", (year, month, day, hour, minute)).fetchone()
            is_open = True if slot_to_book[1] == 0 else False
            slot_id = slot_to_book[0]
            cur.execute("UPDATE calendar SET is_open=0 WHERE slot_id=?;", (slot_id,))
            cur.execute("INSERT INTO appointments (user_id, slot_id, manicure, pedicure, message, is_seen, is_aproved, is_canceled, amount_time_min) VALUES (?, ?, ?, ?, ?, 0, 0, 0, 120);", (session.get("user_id"), slot_id, manicure, pedicure, message))
            con.commit()
            con.close()
            return redirect("/appointments/")
        
        except Exception as er:
            con.close()
            print("##/book/ -- db query")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")        

    else:
        return redirect("/")
