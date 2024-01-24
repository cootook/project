import datetime
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session


def all_appointments():
    today = datetime.datetime.now()
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        user_appoint_db = cur.execute("SELECT user_id, id, manicure, pedicure, message, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month=? AND day>=?) OR slot_id IN (SELECT slot_id FROM calendar WHERE year=? AND month>?) OR slot_id IN (SELECT slot_id FROM calendar WHERE year>?);", (today.year, today.month, today.day, today.year, today.month, today.year)).fetchall()
        user_appoint = []
        for appointment in user_appoint_db:
            if appointment[8] == 0 and appointment[6] == 0: # check if was canceled
                user_name_inst_tel = list(cur.execute("SELECT name, instagram, tel FROM users WHERE id=?", (appointment[0],)).fetchone())
                slot_db = list(cur.execute("SELECT year, month, day, hour, minute FROM calendar WHERE slot_id=?", (appointment[5],)).fetchone())
                user_id = appointment[0]
                appointment_as_list = []
                for el in appointment:
                    el = '-' if el == None else el
                    appointment_as_list.append(el)
                temp = []
                temp.append(user_name_inst_tel[0])
                temp = temp + appointment_as_list[1:2]
                servise_name = ""
                if appointment_as_list[2] == 1 and appointment_as_list[3] == 1:
                    servise_name = "combo"
                elif appointment_as_list[2] == 1 and not appointment_as_list[3] == 1:
                    servise_name = "manicure"
                else:
                    servise_name = "pedicure"
                temp.append(servise_name)
                temp = temp + appointment_as_list[5:len(appointment_as_list)]
                temp = temp + slot_db
                temp.append(appointment_as_list[4])
                temp.append(user_name_inst_tel[1])
                temp.append(user_name_inst_tel[2])
                
                date_for_templete = datetime.datetime(temp[8], temp[9], temp[10])
                time_for_templete = datetime.time(temp[11], temp[12])
                datetime_for_template = datetime.datetime.combine(date_for_templete.date(), time_for_templete)
                temp.append(datetime_for_template.strftime("%a %d %b - %I:%M %p"))
                temp.append(user_id)
                user_appoint.append(temp)
        user_appoint_sorted = sorted(user_appoint, key = lambda x: (x[8], x[9], x[10], x[11], x[12]))
    except Exception as er:
        con.close()
        print("##/all_appointments/ --db connection")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
         

    return render_template("all_appointments.html", user_appoint=user_appoint_sorted)

