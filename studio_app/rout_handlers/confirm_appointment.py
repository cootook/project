from ..services.appointment_service import AppointmentService
from flask import redirect, request, Response
from typing import Tuple, Union
from http import HTTPStatus
from ..error_handlers.appointment_error_handler import AppointmentErrorHandler

appointment_error_handler = AppointmentErrorHandler()

def confirm_appointment() -> Tuple[Union[Response, str], int]:
    try:
        confirmation_data = _extract_confirmation_data()
        return _process_confirmation(confirmation_data)
    except ValueError as e:
        return appointment_error_handler.handle_appointment_error(
            error=e,
            appointment_id=request.form.get("booking_id_confirm", 0),
            additional_data={'user_id': request.form.get("user_id_confirm", 0)}
        )

def _extract_confirmation_data() -> dict:
    try:
        return {
            'user_id': int(request.form.get("user_id_confirm")),
            'appointment_id': int(request.form.get("booking_id_confirm"))
        }
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse form data: {str(e)}")

def _process_confirmation(data: dict) -> Tuple[Union[Response, str], int]:
    appointment_service = AppointmentService()
    success = appointment_service.confirm_booking(
        data['appointment_id'],
        data['user_id']
    )

    if success:
        print(f"Successfully confirmed appointment {data['appointment_id']}")
        return redirect("/all_appointments/"), HTTPStatus.OK
    
    return appointment_error_handler.handle_appointment_error(
        error=ValueError("User ID mismatch or appointment not found"),
        appointment_id=data['appointment_id'],
        additional_data={
            'user_id': data['user_id']
        }
    )