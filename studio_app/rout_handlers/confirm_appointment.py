from ..services.appointment_service import AppointmentService
from flask import redirect, render_template, request, Response
from typing import Tuple, Union
from http import HTTPStatus

def confirm_appointment():
    try:
        confirmation_data = _extract_confirmation_data
        return _process_confirmation(confirmation_data)
    except Exception as er:
        print("##/confirm_appointment/ --form request")
        print(er)
        return  render_template("apology.html", error_message="Something went wrong")
    
    db_base.session.execute(update(Appointment).where(Appointment.id == booking_id_confirm, Appointment.user_id == user_id_confirm).values(
        approved = True,
        last_update_at = datetime.datetime.now(),
        last_update_by_id = current_user.id,
        approved_at = datetime.datetime.now(),
        approved_by_id = current_user.id
        ))
    db_base.session.commit()


    return redirect("/all_appointments/")

def _extract_confirmation_data(data: dict) -> dict:
    try:
        return {
            'user_id': int(request.form.get("user_id_confirm")),
            'appointment_id': int(request.form.get("booking_id_confirm"))
        }
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse form data: {str(e)}")

def _process_confirmation(data: dict) -> Tuple[Union[Response, str], int]:
    appointment_service = AppointmentService()