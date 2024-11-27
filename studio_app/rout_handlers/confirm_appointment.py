import datetime

from sqlalchemy import update
from studio_app.db_classes import Appointment, db_base
from flask import redirect, render_template, request
from flask_security import current_user


def confirm_appointment():
    try:
        user_id_confirm = int(request.form.get("user_id_confirm"))
        booking_id_confirm = int(request.form.get("booking_id_confirm"))
        
        print(user_id_confirm, booking_id_confirm)
        
    except Exception as er:
        print("##/confirm_appointment/ --form request")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
    
    db_base.session.execute(update(Appointment).where(Appointment.id == booking_id_confirm, Appointment.user_id == user_id_confirm).values(
        approved = True,
        lust_update_at = datetime.datetime.now(),
        lust_update_by_id = current_user.id,
        approved_at = datetime.datetime.now(),
        approved_by_id = current_user.id
        ))
    db_base.session.commit()


    return redirect("/all_appointments/")

