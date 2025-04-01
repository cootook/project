from flask import flash, redirect, render_template, request, url_for

from ..validations.forms.appointment_forms import ConfirmAppointmentViaSms
from ..services.appointment_service import AppointmentService
from ..services.slot_service import SlotService
from ..repositories.slot_repository import SlotRepository
from ..repositories.appointment_repository import AppointmentRepository

def sms_confirmation_of_booking():
    form = ConfirmAppointmentViaSms()
    
    if request.method == "GET":
        appointment_id = request.args.get("appointment_id")
        form.appointment_id.data = appointment_id
        appointment_service = AppointmentService()
        flash(f"code was sent to {appointment_service.get_user_phone_by_appointment_id(appointment_id)}")
        return render_template("booking_sms_confirmation_code.html", form=form)
    if form.validate_on_submit():
        appointment_service = AppointmentService()
        appointment_repo = AppointmentRepository()
        slot_service = SlotService()
        slot_repo = SlotRepository()

        appointment = appointment_repo.get_by_id(form.appointment_id.data)
        slot = slot_repo.get_by_id(appointment.slot_id) 

        appointment_service.set_phone_confirmed_by_appointment_id(appointment.id)
        slot_service.reserve_slot(slot.id, appointment.id) 
        
        return render_template("message_page.html", message_title="success", 
                                        message_header=f"Your request for {str(appointment.service).lstrip("[").rstrip("]")} on", 
                                        message_text= f"""  {slot.date.strftime("%d %B, %Y")} 
                                        at {slot.time.strftime("%I:%M%p").lstrip('0')} was sent.
                                          We will review the request and contact you as soon as possible.
                                          Thank you!""", 
                                        message_link="/", 
                                        message_link_text="Home page.")
    else:
        flash("wrong code", "error")
        return redirect(url_for(
                "sms_confirmation",
                appointment_id=form.appointment_id.data
            ))