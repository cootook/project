import datetime

from flask import redirect, render_template, request, url_for
from ..services.phone_service import PhoneNumberService
from ..services.verification_service import SmsVerification
from ..services.booking_service import Booking
from ..services.service_service import ServiceService
from ..validations.forms.appointment_forms import BookAppointmentForm

def book():    
    service_service = ServiceService()
    form = BookAppointmentForm()

    if request.method == "GET":
        slot_id = request.args.get("slot_id")
        date_time_iso = request.args.get("datetime-iso")

        list_of_available_services = service_service.get_list_of_active_services()

        form.service.choices = list_of_available_services
        form.date_time_iso.data = datetime.datetime.strptime(date_time_iso, "%Y-%m-%dT%H:%M:%S")
        form.slot_id.data = slot_id

        return render_template("book.html", form=form)
    else:
        if form.validate_on_submit():
            phone_service = PhoneNumberService(form.full_phone.data) 

            booking_service = Booking(
                form.date_time_iso.data,
                form.slot_id.data,
                form.message.data,
                phone_service.canonical,
                form.name.data,
                [form.service.data]
            )

            sms_verification = SmsVerification(
                booking_service.client_phone,
                booking_service.confirmation_code
                )
            message_instance = sms_verification.send_code()   

            return redirect(url_for(
                "sms_confirmation",
                appointment_id=booking_service.appointment_id
            ))
        else:
            return render_template("apology.html", error_message="something went wrong")
  