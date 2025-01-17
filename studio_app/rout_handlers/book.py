import datetime
import json
import os
import phonenumbers

from flask import redirect, render_template, request, session, current_app
from flask_security import current_user, hash_password, login_user, logout_user
from ..helpers_legacy import validate_recaptcha, send_sms
from random import randrange
from sqlalchemy import select, update
from studio_app.db_classes import Appointment, Slot, Service, db_base, User



def book():
    
    if request.method == "POST":
        try:                  
            form_data = request.form.to_dict()
            token = request.form.get("g-recaptcha-response")
            datetime_iso = request.form.get("datetime-iso")
            slot_id = int(request.form.get("slot_id"))
            message = request.form.get("message-text")
            full_phone = request.form.get("full_phone") 
            client_name = request.form.get("client_name")         
            print("## - form:", form_data)
        except Exception as er:
            print("##/book/ --request.form.get")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong") 

        if not validate_recaptcha(token):
            return  render_template("apology.html", error_message="Sorry. Something went wrong with anti robot, maybe reCaptcha that you have just checked expired. Please, try again or contact us.")
        
        parsed_phone = phonenumbers.parse(full_phone, None)
        is_number_valid = phonenumbers.is_valid_number(parsed_phone)
        if not is_number_valid:
            print("phone validation FAILED")
            return  render_template("apology.html", error_message=f"Sorry {client_name}. We cannot sent a message to {full_phone}. Please, try again or contact us.")
        
        canonical_n = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)

        try:
            requested_date_time = datetime.datetime.strptime(datetime_iso, "%Y-%m-%dT%H:%M:%S")
            requested_date = requested_date_time.date()
            requested_time = requested_date_time.time()
        except Exception as er:
            print(f"cannot get date out of submitted datetime_iso: {datetime_iso}")
        print(slot_id, requested_date, requested_time)
        requested_slot = Slot.query.filter(Slot.id == slot_id, Slot.date == requested_date, Slot.time == requested_time, Slot.opened == True).first()  
        if requested_slot is None:
            return  render_template("apology.html", error_message="Sorry. This slot is not available. Please, try again or contact us.")        

        service_list = []
        for item in form_data:
            if item == form_data[item]:
                service_by_name = db_base.session.scalar(select(Service).where(Service.name == item, Service.deleted == False))
                if not service_by_name == None:
                    service_list.append(item)
        # find or create user
        logout_user()
        client = db_base.session.scalar(select(User).where(User.tel == canonical_n))
        if client is None:
            from studio_app.webapp import user_datastore
            # client = User(tel = canonical_n, name = client_name, email = os.environ.get("DEFAULT_EMAIL"), password = hash_password(os.environ.get("DEFAULT_PASSWORD")))
            client = user_datastore.create_user(tel = canonical_n, name = client_name, email = os.environ.get("DEFAULT_EMAIL"), password = hash_password(os.environ.get("DEFAULT_PASSWORD")))
            db_base.session.add(client)
            db_base.session.commit()
            user_datastore.add_role_to_user(client, "client")
        login_user(client)
        new_appointment = Appointment.create(current_user.id, json.dumps(service_list), requested_date_time, slot_id, message)
        sms_confirmation_code = randrange(1000, 9999, 11)

        db_base.session.execute(update(Appointment).where(Appointment.id == new_appointment.id).values(sms_confirmation_code = sms_confirmation_code))

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
