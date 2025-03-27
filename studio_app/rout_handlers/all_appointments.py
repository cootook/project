from flask import render_template, request
from ..services.appointment_service import AppointmentService


def all_appointments():
    try:
        page = int(request.args.get('page', 1, type=int))
        per_page = int(request.args.get('per_page', 50, type=int))
        
        if page < 1 or per_page < 1:
            return render_template(
            "apology.html",
            error_message="Invalid pagination parameters"
        ), 400

        appointment_service = AppointmentService()
        appointments_data = appointment_service.get_all_as_list(page, per_page)
        appointments_json = appointment_service.format_appointments_for_frontend(appointments_data)
        
        return render_template(
            "all_appointments.html",
            user_appointments_for_frontend=appointments_json,
            user_appointments_for_template=appointments_data['appointments']
        )

    except Exception as e:
        print(f"Error in list_appointments: {str(e)}")
        return render_template(
            "apology.html",
            error_message="Failed to load appointments"
        ), 500

