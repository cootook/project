import datetime
import sqlite3

from flask import redirect, render_template, request, session
from studio_app.helpers import get_service_name

def appointments():
    today = datetime.datetime.now()
    try:
        con = sqlite3.connect("./db.db") 
        cur = con.cursor()
        user_id = session.get("user_id")
        user_appoint_db = cur.execute("SELECT id, manicure, pedicure, message, slot_id, is_seen, is_aproved, is_canceled, amount_time_min FROM appointments WHERE user_id=? AND slot_id IN (SELECT slot_id FROM calendar WHERE (year=? AND month=? AND day>=?) OR (year=? AND month>?) or (year>?));", (user_id, today.year, today.month, today.day, today.year, today.month, today.year)).fetchall()
        user_name_inst_tel = cur.execute("SELECT name, instagram, tel FROM users WHERE id=?", (user_id,)).fetchone()
        user_appoint_list_dict = []
        user_dict = {}
        user_dict["id"] = user_id
        user_dict["name"] = '-' if user_name_inst_tel[0] == None else user_name_inst_tel[0]
        user_dict["instagram"] = user_name_inst_tel[1]
        user_dict["tel"] = user_name_inst_tel[2]
        for appointment in user_appoint_db:
            if appointment[7] == 0:
                temp_dict = {}                
                temp_dict["slot_id"] = appointment[4]
                temp_dict["service"] = get_service_name(appointment[1], appointment[2])
                temp_dict["message"] = '-' if appointment[3] == None else appointment[3]
                temp_dict["done"] = appointment[5]
                temp_dict["confirmed"] = appointment[6]
                temp_dict["canceled"] = appointment[7]
                temp_dict["duretion"] = appointment[8]
                slot_db = list(cur.execute("SELECT year, month, day, hour, minute FROM calendar WHERE slot_id=?", (appointment[4],)).fetchone())
                temp_dict["year"] = slot_db[0]
                temp_dict["month"] = slot_db[1]
                temp_dict["day"] = slot_db[2]
                temp_dict["hour"] = slot_db[3]
                temp_dict["minute"] = slot_db[4]
                date_for_templete = datetime.datetime(slot_db[0], slot_db[1], slot_db[2])
                time_for_templete = datetime.time(slot_db[3], slot_db[4])
                datetime_for_template = datetime.datetime.combine(date_for_templete.date(), time_for_templete)
                temp_dict["full_date_time"] = datetime_for_template.strftime("%a %d %b - %I:%M %p")                               
                user_appoint_list_dict.append(temp_dict)
        user_appoint_list_dict_sorted = sorted(user_appoint_list_dict, key = lambda x: (x["year"], x["month"], x["day"], x["hour"], x["minute"]))
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

    return render_template("appointments.html", user_appoint=user_appoint_list_dict_sorted, user=user_dict)
