import datetime

from flask import redirect, render_template, request, session
from ..services.recaptcha_service import RecaptchaService
from ..services.phone_service import PhoneNumberService
from ..services.verification_service import SmsVerificationOfBooking
from ..services.booking_service import Booking
from ..models.service import ServiceModel
from ..services.service_service import ServiceService
from ..validations.forms.appointment_forms import BaseAppointmentForm

def book():    
    if request.method == "POST":
        try:                  
            form_data = request.form.to_dict()
            token = request.form.get("g-recaptcha-response")
            input_datetime_iso = request.form.get("datetime-iso")
            slot_id = int(request.form.get("slot_id"))
            message = request.form.get("message-text")
            terms_and_privacy = request.form.get("terms_and_privacy")       
            input_phone = request.form.get("full_phone") 
            client_name = request.form.get("client_name")         
            print("## - form:", form_data)
        except Exception as er:
            print("##/book/ --request.form.get")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong") 

        if not RecaptchaService.validate(token):
            return  render_template(
                "apology.html", 
                error_message="Sorry. Something went wrong with anti robot, maybe reCaptcha that you have just checked expired. Please, try again or contact us."
                )
        service_for_services = ServiceService()

        phone = PhoneNumberService(input_phone)

        if not phone.is_valid:
            return  render_template(
                "apology.html", 
                error_message=f"Sorry {client_name}. We cannot sent a message to {input_phone}. Please, try again or contact us."
                )

        try:
            booking_datetime = datetime.datetime.strptime(input_datetime_iso, "%Y-%m-%dT%H:%M:%S")
        except Exception as er:
            print(f"cannot get date out of submitted input_datetime_iso: {input_datetime_iso}")
            return  render_template(
                "apology.html",
                error_message="Something gone wrong. Please, try again or contact us."
                )

        list_of_requested_services = service_for_services.get_list_of_services_from_form_data_dict(form_data) 
        new_booking = Booking(
            booking_datetime, 
            slot_id, message, 
            phone.canonical, 
            client_name, 
            list_of_requested_services
            )       

        new_verification = SmsVerificationOfBooking(new_booking)
        new_verification.send_code()

        session["booking_json"] = new_booking.to_json()

        return render_template(
            "booking_sms_confirmation_code.html", 
            phone=new_booking.client_phone,
            name=new_booking.client_name
            )

    else:
        form = BaseAppointmentForm()
        # get slot id
        # get date
        return render_template(
            "book.html", 
            form=form
            )
