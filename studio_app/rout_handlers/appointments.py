import datetime
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from studio_app.helpers import get_service_name


def appointments():
    today = datetime.datetime.now()
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        user_appoint_db = cur.execute("SELECT id, manicure, pedicure, message, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE (year=? AND month=? AND day>=?) OR (year=? AND month>?) or (year>?));", (session.get("user_id"), today.year, today.month, today.day, today.year, today.month, today.year)).fetchall()
        user_appoint = []
        for appointment in user_appoint_db:
            if appointment[7] == 0:
                slot_db = list(cur.execute("SELECT year, month, day, hour, minute FROM calendar WHERE slot_id=?", (appointment[4],)).fetchone())
                appointment_as_list = []
                for el in appointment:
                    el = '-' if el == None else el
                    appointment_as_list.append(el)
                appointment_as_list = appointment_as_list + slot_db
                temp = []
                print(appointment)
                temp.append(appointment_as_list[0])
                temp.append(get_service_name(appointment_as_list[1], appointment_as_list[2]))
                temp = temp + appointment_as_list[4:14]
                temp.append(appointment_as_list[3])
                print(temp)
                user_appoint.append(temp)
        user_appoint_sorted = sorted(user_appoint, key = lambda x: (x[7], x[8], x[9], x[10], x[11]))
    except Exception as er:
        con.close()
        print("##/appointments/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
       

    if request.method == "POST":
        try:
            appointment_id_to_cancel = int(request.form.get("appointment_id"))
            print("canceled appointment, id:")
            print(appointment_id_to_cancel)

            cur.execute("UPDATE appointments SET is_canceled=1 WHERE id=?", (appointment_id_to_cancel,))
            con.commit()
            con.close()
            return redirect("/appointments/")

        except Exception as er:
            con.close()
            print("##/appointments/ --cancell")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")

    return render_template("appointments.html", user_appoint=user_appoint_sorted)
