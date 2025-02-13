from ..services.appointment_service import AppointmentService
from flask import redirect, render_template, request, Response
from typing import Tuple, Union
from http import HTTPStatus

def cancel_appointment():
    try:
        cancellation_data = _extract_cancellation_data()
        return _process_cancellation(cancellation_data)
    except ValueError as e:
        return _handle_error(f"Invalid form data: {str(e)}", HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return _handle_error(f"Unexpected error: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
    
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
    
    return _handle_error(
        "Failed to cancel appointment - user ID mismatch or appointment not found",
        HTTPStatus.NOT_FOUND
    )

def _handle_error(message: str, status_code: int) -> Tuple[str, int]:
    print(f"ERROR: /cancel_appointment/ - {message}")
    return render_template("apology.html", error_message=message), status_code
