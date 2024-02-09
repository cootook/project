import sqlite3

from flask import redirect, render_template, request

def edit_appointment():
    try:
        # new_date: 2023-12-31
        # new_time: 10:00
        # new_duration: 120
        # new_manicure: on / None
        # new_pedicure: on / None
        # new_message: 
        # user_id_edit: 1
        # booking_id_edit: 301
        new_date = request.form.get("new_date")
        new_time = request.form.get("new_time")
        new_duration = int(request.form.get("new_duration"))
        new_manicure = 1 if request.form.get("new_manicure") is not None else 0
        new_pedicure = 1 if request.form.get("new_pedicure") is not None else 0
        new_message = request.form.get("new_message")
        user_id_edit = int(request.form.get("user_id_edit"))
        booking_id_edit = int(request.form.get("booking_id_edit"))
        print("#edit - new_date, new_time, new_duration, new_manicure, new_pedicure, new_message, user_id_edit, booking_id_edit")
        print(new_date, new_time, new_duration, new_manicure, new_pedicure, new_message, user_id_edit, booking_id_edit)
        new_year = int(new_date[0:4])
        new_month = int(new_date[5:7]) 
        new_day = int(new_date[8:10]) 
        new_hour = int(new_time[0:2]) 
        new_minute = int(new_time[3:5]) 
        print("#edit - new_year, new_day, new_month, new_hour, new_minute")
        print(new_year, new_day, new_month, new_hour, new_minute)
        
    except Exception as er:
        print("##/edit_appointment/ --form request")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
    
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        # appointments (
        #     id INTEGER PRIMARY KEY, 
        #     user_id INT, 
        #     pedicure INT, 
        #     manicure INT, 
        #     message TEXT, 
        #     slot_id INT, 
        #     amount_time_min INT, 
        #     slots_in TEXT, 
        #     is_seen INT, 
        #     is_aproved INT, 
        #     is_canceled INT, 
        #     FOREIGN KEY (slot_id) REFERENCES calendar(slot_id), 
        #     FOREIGN KEY (user_id) REFERENCES users(id))
        print("#id edit - ", booking_id_edit)
        cur.execute("UPDATE appointments SET pedicure=?, manicure=?, message=?, amount_time_min=? WHERE user_id=? AND slot_id=?", (new_pedicure, new_manicure, new_message, new_duration, user_id_edit, booking_id_edit))
        #  calendar(slot_id INTEGER PRIMARY KEY, year INT, month INT, weekday INT, day INT, hour INT, minute INT, is_open INT);
        cur.execute("UPDATE calendar SET year=?, month=?, day=?, hour=?, minute=?, is_open=0 WHERE slot_id=?", (new_year, new_month, new_day, new_hour, new_minute, booking_id_edit))
        con.commit()
        con.close()
        return redirect("/all_appointments/")
        
    except Exception as er:
        con.close()
        print("##/edit_appointment/ --db")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
