import datetime

from sqlalchemy import update, select
from studio_app.db_classes import Appointment, db_base
from flask import redirect, render_template, request
from flask_security import current_user
from flask import redirect, render_template, request

def cancel_appointment():
    try:
        user_id_cancel = int(request.form.get("user_id_cancel"))
        booking_id_cancel = int(request.form.get("booking_id_cancel"))
        cancel_message = request.form.get("cancel_message")

    except Exception as er:
        print("##/cancel_appointment/ --form request")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
    messages = db_base.session.scalar(select(Appointment.description).where(Appointment.id == booking_id_cancel, Appointment.user_id == user_id_cancel))
    db_base.session.execute(update(Appointment).where(Appointment.id == booking_id_cancel, Appointment.user_id == user_id_cancel).values(
        description = cancel_message + " | " + messages,
        last_update_at = datetime.datetime.now(),
        last_update_by_id = current_user.id,
        canceled_at = datetime.datetime.now(),
        canceled_by_id = current_user.id,
        canceled = True
        ))
    db_base.session.commit()
    
    return redirect("/all_appointments/")
