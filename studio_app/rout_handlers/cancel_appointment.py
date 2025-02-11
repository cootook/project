from ..services.appointment_service import AppointmentService
from flask import redirect, render_template, request

def cancel_appointment():
    try:
        user_id_cancel = int(request.form.get("user_id_cancel"))
        booking_id_cancel = int(request.form.get("booking_id_cancel"))
        cancel_message = request.form.get("cancel_message")

    except Exception as er:
        print("ERROR: /cancel_appointment/ --form request: ", er)
        return  render_template("apology.html", error_message="Something went wrong"), 400
    
    appointment_service = AppointmentService()
    success_cancel = appointment_service.cancel_with_message(
        booking_id_cancel, 
        user_id_cancel, 
        cancel_message
        )
    if success_cancel:
        print(f"CANCELED appointment {booking_id_cancel}")
        return redirect("/all_appointments/"), 200
    else:
        print("ERROR: /cancel_appointment/ .cancel_with_message ")
        return  render_template("apology.html", error_message="Something went wrong"), 500
