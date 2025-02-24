from flask import redirect, request
from ..services.appointment_service import AppointmentService
from flask import redirect, request, Response
from typing import Tuple, Union
from http import HTTPStatus
from ..error_handlers.appointment_error_handler import AppointmentErrorHandler

appointment_error_handler = AppointmentErrorHandler()

def done_appointment() -> Tuple[Union[Response, str], int]:
    try:
        data = _extract_cancellation_data()
        appointment_service = AppointmentService()
        appointment_service.set_as_done_with_price(
            data['booking_id'],
            data['user_id'],
            data['price']
        )
    except ValueError as e:
        return appointment_error_handler.handle_appointment_error(
            error=e,
            appointment_id=data.get('booking_id_done'),
            additional_data={'user_id': data.get('user_id')}
        )
    
    return redirect("/all_appointments/"), HTTPStatus.OK

def _extract_cancellation_data() -> dict:
    try:
        return {
            'user_id': int(request.form.get("user_id_done")),
            'booking_id': int(request.form.get("booking_id_done")),
            'price': float(request.form.get("done_price", 0))
        }
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse form data: {str(e)}")