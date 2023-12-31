import sqlite3

from flask import redirect, render_template, request

def done_appointment():
    try:
        user_id_done = int(request.form.get("user_id_done"))
        booking_id_done = int(request.form.get("booking_id_done"))
        
        print(user_id_done, booking_id_done)
        
    except Exception as er:
        print("##/done_appointment/ --form request")
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
        cur.execute("UPDATE appointments SET is_seen=1 WHERE user_id=? AND slot_id=?", (user_id_done, booking_id_done))
        con.commit()
        con.close()
        return redirect("/all_appointments/")
        
    except Exception as er:
        con.close()
        print("##/done_appointment/ --db")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")