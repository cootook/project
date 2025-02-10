import datetime

from json import dumps
from sqlalchemy import select, update
from studio_app.db_classes import Appointment, Service, db_base
from flask import redirect, render_template, request
from flask_security import current_user

def edit_appointment():
    form = request.form
    new_date = request.form.get("new_date")
    new_date_py = datetime.datetime.strptime(new_date, '%Y-%m-%dT%H:%M')
    new_duration = int(request.form.get("new_duration"))
    new_message = request.form.get("new_message")
    user_id_edit = int(request.form.get("user_id_edit"))
    booking_id_edit = int(request.form.get("booking_id_edit"))
    
    services = db_base.session.scalars(select(Service.name).where(Service.deleted == False))
    list_of_services = []
    for s in services:
        list_of_services.append(s)

    new_service = []
    for s in list_of_services:
        if s in form:
            new_service.append(s)
    appointment_to_edit = db_base.session.scalar(select(Appointment).where(Appointment.id == booking_id_edit, Appointment.user_id == user_id_edit))

    if appointment_to_edit is None:
        return render_template("apology.html", error_message="Sorry. Something went wrong. Please, try again later.")
    else:
        messages = db_base.session.scalar(select(Appointment.description).where(Appointment.id == booking_id_edit, Appointment.user_id == user_id_edit))
        db_base.session.execute(update(Appointment).where(Appointment.id == booking_id_edit, Appointment.user_id == user_id_edit).values(
            at = new_date_py,
            amount_time_min = new_duration,
            description = new_message + " | " + messages,
            service = dumps(new_service),
            last_update_at = datetime.datetime.now(),
            last_update_by_id = current_user.id
        ))
        db_base.session.commit()
      
    return redirect("/all_appointments/")
