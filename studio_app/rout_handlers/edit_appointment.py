import datetime

from json import dumps
from sqlalchemy import select, update
from studio_app.db_classes import Appointment, Service, db_base
from flask import redirect, render_template, request
from flask_security import current_user

from flask import redirect, request
from ..services.appointment_service import AppointmentService
from flask import redirect, request, Response
from typing import Tuple, Union
from http import HTTPStatus
from ..error_handlers.appointment_error_handler import AppointmentErrorHandler
from ..services.service_service import ServiceService
from ..repositories.service_repository import ServiceRepository

appointment_error_handler = AppointmentErrorHandler()
service_for_services = ServiceService()
service_repo = ServiceRepository()


def edit_appointment() -> Tuple[Union[Response, str], int]:
    try:
        data = _extract_new_data()
        new_date_time_pythonic = datetime.datetime.strptime(
            data['date_time'], 
            '%Y-%m-%dT%H:%M'
            )
    # check if appointment exists
    # get old description
    # append old description to new message
    # update appointment 
        # messages = db_base.session.scalar(select(Appointment.description).where(Appointment.id == booking_id_edit, Appointment.user_id == user_id_edit))
        # db_base.session.execute(update(Appointment).where(Appointment.id == booking_id_edit, Appointment.user_id == user_id_edit).values(
        #     at = new_date_py,
        #     amount_time_min = new_duration,
        #     description = new_message + " | " + messages,
        #     service = dumps(new_service),
        #     last_update_at = datetime.datetime.now(),
        #     last_update_by_id = current_user.id
        # ))
    except ValueError as e:
        return appointment_error_handler.handle_appointment_error(
            error=e,
            appointment_id=data.get('booking_id'),
            additional_data={'user_id': data.get('user_id')}
        )
      
    return redirect("/all_appointments/"), HTTPStatus.OK

def _extract_new_data() -> dict:
    try:
        return {
            'user_id': int(request.form.get("user_id_edit")),
            'booking_id': int(request.form.get("booking_id_edit")),
            'message': float(request.form.get("new_message", "")),
            'duration': int(request.form.get("new_duration")),
            'date_time': request.form.get("new_date"),
            'service': service_for_services.get_list_of_services_from_form_data_dict(request.form)
        }
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse form data: {str(e)}")
