from ..services.appointment_service import AppointmentService
from flask import redirect, request, Response
from typing import Tuple, Union
from http import HTTPStatus
from ..error_handlers.appointment_error_handler import AppointmentErrorHandler

appointment_error_handler = AppointmentErrorHandler()

def cancel_appointment():
    try:
        cancellation_data = _extract_cancellation_data()
        return _process_cancellation(cancellation_data)
    except ValueError as e:
        return appointment_error_handler.handle_appointment_error(
            error=e,
            appointment_id=cancellation_data.get('appointment_id'),
            additional_data={'user_id': cancellation_data.get('user_id')}
        )
def _extract_cancellation_data() -> dict:
    try:
        return {
            'user_id': int(request.form.get("user_id_cancel")),
            'booking_id': int(request.form.get("booking_id_cancel")),
            'message': request.form.get("cancel_message")
        }
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse form data: {str(e)}")
    
def _process_cancellation(data: dict) -> Tuple[Union[Response, str], int]:
    appointment_service = AppointmentService()
    success = appointment_service.cancel_with_message(
        data['booking_id'],
        data['user_id'],
        data['message']
    )
    
    if success:
        print(f"Successfully canceled appointment {data['booking_id']}")
        return redirect("/all_appointments/"), HTTPStatus.OK
    
    return appointment_error_handler.handle_appointment_error(
        error=ValueError("User ID mismatch or appointment not found"),
        appointment_id=data['booking_id'],
        additional_data={
            'user_id': data['user_id']
        }
    )
