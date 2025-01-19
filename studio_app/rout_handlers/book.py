import datetime
import json
import os
import phonenumbers

from flask import redirect, render_template, request, session, current_app, g as global_store
from flask_security import current_user, hash_password, login_user, logout_user
from ..helpers_legacy import send_sms
from ..helpers.recaptcha import Recaptcha
from ..helpers.phone import Phone
from ..services.booking import Booking
from random import randrange
from sqlalchemy import select, update
from studio_app.db_classes import Appointment, Slot, Service, db_base, User



def book():
    
    if request.method == "POST":
        try:                  
            form_data = request.form.to_dict()
            token = request.form.get("g-recaptcha-response")
            input_datetime_iso = request.form.get("datetime-iso")
            slot_id = int(request.form.get("slot_id"))
            message = request.form.get("message-text")
            input_phone = request.form.get("full_phone") 
            client_name = request.form.get("client_name")         
            print("## - form:", form_data)
        except Exception as er:
            print("##/book/ --request.form.get")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong") 

        if not Recaptcha.validate(token):
            return  render_template(
                "apology.html", 
                error_message="Sorry. Something went wrong with anti robot, maybe reCaptcha that you have just checked expired. Please, try again or contact us."
                )
        
        phone = Phone(input_phone)

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

        list_of_requested_services = Service.get_list_of_services_from_dict(form_data)

        # find or create user
        # logout_user()
        # client = db_base.session.scalar(select(User).where(User.tel == canonical_n))
        # if client is None:
        #     from studio_app.webapp import user_datastore
        #     # client = User(tel = canonical_n, name = client_name, email = os.environ.get("DEFAULT_EMAIL"), password = hash_password(os.environ.get("DEFAULT_PASSWORD")))
        #     client = user_datastore.create_user(tel = canonical_n, name = client_name, email = os.environ.get("DEFAULT_EMAIL"), password = hash_password(os.environ.get("DEFAULT_PASSWORD")))
        #     db_base.session.add(client)
        #     db_base.session.commit()
        #     user_datastore.add_role_to_user(client, "client")
        # login_user(client)
        # new_appointment = Appointment.create(current_user.id, json.dumps(service_list), requested_date_time, slot_id, message)
        # sms_confirmation_code = randrange(1000, 9999, 11)

        # db_base.session.execute(update(Appointment).where(Appointment.id == new_appointment.id).values(sms_confirmation_code = sms_confirmation_code))
        global_store.booking = Booking(
            booking_datetime, 
            slot_id, message, 
            phone.canonical, 
            client_name, 
            list_of_requested_services
            )
        return render_template(
            "booking_sms_confirmation_code.html", 
            appointment_id=global_store.booking.slot_id, 
            phone=global_store.booking.client_phone
            )
        if Slot.book(current_user.id, requested_slot, new_appointment):
            sms_link = os.environ.get("TWILIO_SITE_LINK")
            sms_business_name = os.environ.get("TWILIO_BUSINESS_NAME")
            code_sms_text = f"Your {sms_business_name} confirmation code is {sms_confirmation_code} . Visit {sms_link}. STOP to cancel."
            send_code = send_sms(os.environ.get("TWILIO_FROM_NUMBER"), canonical_n, code_sms_text)
            return render_template("booking_sms_confirmation_code.html", appointment_id=slot_id, phone=canonical_n)
            return render_template("message_page.html", message_title="success", 
                                                    message_header="You requested appointment on", 
                                                    message_text= " " + requested_date.strftime("%m/%d/%Y") + " at " + requested_time.strftime("%H:%M") + ". We will send you a confirmation.", 
                                                    message_link="/", 
                                                    message_link_text="Home page.")
        else:
            return  render_template("apology.html", error_message="Something went wrong")

    else:
        return redirect("/")
