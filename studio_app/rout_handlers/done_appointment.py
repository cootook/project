import datetime

from sqlalchemy import update
from studio_app.db_classes import Appointment, db_base
from flask import redirect, render_template, request
from flask_security import current_user
from flask import redirect, render_template, request

def done_appointment():
    try:
        user_id_done = int(request.form.get("user_id_done"))
        booking_id_done = int(request.form.get("booking_id_done"))
        price_done = request.form.get("done_price")
        print(user_id_done, booking_id_done, price_done)
        
    except Exception as er:
        print("##/done_appointment/ --form request")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
    
    db_base.session.execute(update(Appointment).where(Appointment.id == booking_id_done, Appointment.user_id == user_id_done).values(
        last_update_at = datetime.datetime.now(),
        last_update_by_id = current_user.id,
        done_at = datetime.datetime.now(),
        done_by_id = current_user.id,
        price = price_done,
        done = True
        ))
    db_base.session.commit()
    
    return redirect("/all_appointments/")