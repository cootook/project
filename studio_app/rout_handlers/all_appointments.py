from flask import render_template
from ..services.appointment_service import AppointmentService


def all_appointments():
    appointment_service = AppointmentService()
    appointments_list = appointment_service.get_all_as_list()
    appointments_js = appointment_service.get_js_object_out_of_list_of_appointments(appointments_list)
    
    return render_template(
        "all_appointments.html",
        user_appointments_for_frontend=appointments_js,
        user_appointments_for_template=appointments_list
    )
