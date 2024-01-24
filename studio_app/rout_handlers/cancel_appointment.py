import sqlite3

from flask import redirect, render_template, request, session

def cancel_appointment():
    try:
        user_id_cancel = int(request.form.get("user_id_cancel"))
        booking_id_cancel = int(request.form.get("booking_id_cancel"))
        cancel_message = request.form.get("cancel_message")

        if session.get("is_admin") == 0 and user_id_cancel != session.get("user_id"):
            print("##/cancel_appointment/ --Access denied. User # ", session.get("user_id"))
            return  render_template("apology.html", error_message="Access denied.")
        else:
            print(f"#canceling for \nuser #{user_id_cancel} \nbooking id #{booking_id_cancel} \nwith msg: '{cancel_message}',\n by #{session.get("user_id")} is admin - {session.get("is_admin")}")
        
    except Exception as er:
        print("##/cancel_appointment/ --form request")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
    
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        cur.execute("UPDATE appointments SET is_canceled=1, message=? WHERE user_id=? AND slot_id=?", (cancel_message, user_id_cancel, booking_id_cancel))
        con.commit()
        con.close()
        if session.get("is_admin") == 0:
            return redirect("/appointments/")
        else:
            return redirect("/all_appointments/")
        
    except Exception as er:
        con.close()
        print("##/cancel_appointment/ --db")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")