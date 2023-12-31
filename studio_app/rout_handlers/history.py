import datetime
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from studio_app.helpers import get_service_name

def history():
    today = datetime.datetime.now()
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        user_appoint_db = cur.execute("SELECT id, manicure, pedicure, message, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE (year=? AND month=? AND day<?) OR (year=? AND month<?) OR (year<?));", (session.get("user_id"), today.year, today.month, today.day, today.year, today.month, today.year)).fetchall()
        user_appoint_db = user_appoint_db + cur.execute("SELECT id, manicure, pedicure, message, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE is_canceled=? AND user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE (year=? AND month=? AND day>=?) OR (year=? AND month>?) or (year>?));", (1, session.get("user_id"), today.year, today.month, today.day, today.year, today.month, today.year)).fetchall()
        user_appoint = []
        for appointment in user_appoint_db:
            
            slot_db = list(cur.execute("SELECT year, month, day, hour, minute FROM calendar WHERE slot_id=?", (appointment[4],)).fetchone())
            appointment_as_list = []
            for el in appointment:
                el = 'No data' if el == None else el
                appointment_as_list.append(el)
            appointment_as_list = appointment_as_list + slot_db
            temp = []
            temp.append(appointment_as_list[0])
            temp.append(get_service_name(appointment_as_list[1], appointment_as_list[2]))
            temp = temp + appointment_as_list[4:14]
            temp.append(appointment_as_list[3])
            user_appoint.append(temp)
                # (id - 7, service_name - None, slot - 252, seen - 0, aproved - 0, canceled - 1, timing - 120, 2023, 12, 27, 11, 30)
        print(user_appoint)
        user_appoint_sorted = sorted(user_appoint, key = lambda x: (x[9], x[8], x[7], x[10], x[11]))
    except Exception as er:
        con.close()
        print("##/history/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
       
    return render_template("history.html", user_appoint=user_appoint_sorted)