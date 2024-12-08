import datetime
import json

from flask import redirect, render_template, request, session
from ..helpers import validate_recaptcha
from sqlalchemy import select
from studio_app.db_classes import Appointment, Slot, Service, db_base

def book():
    
    if request.method == "POST":
        try:                  
            form_data = request.form.to_dict()
            token = request.form.get("g-recaptcha-response")
            datetime_iso = request.form.get("datetime-iso")
            slot_id = int(request.form.get("slot_id"))
            message = request.form.get("message-text")            

        except Exception as er:
            print("##/book/ --request.form.get")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong") 

        if not validate_recaptcha(token):
            return  render_template("apology.html", error_message="Sorry. Something went wrong with anti robot, maybe reCaptcha that you have just checked expired. Please, try again.")
        
        requested_date_time = datetime.datetime.strptime(datetime_iso, "%Y-%m-%dT%H:%M:%S")
        requested_date = requested_date_time.date()
        requested_time = requested_date_time.time()
        
        # try:
        requested_slot = Slot.query.filter(Slot.id == slot_id, Slot.date == requested_date, Slot.time == requested_time).first()  
        if requested_slot is None:
            return  render_template("apology.html", error_message="Sorry. Something went wrong with this slot. Please, try again.")        
        if not requested_slot.opened:
            return  render_template("apology.html", error_message="Time is not available")
        else:
            # define service 
            service_list = []
            for item in form_data:
                if item == form_data[item]:
                    service_by_name = db_base.session.scalar(select(Service).where(Service.name == item, Service.deleted == False))
                    if not service_by_name == None:
                        service_list.append(item)
            new_appointment = Appointment.create(session["user_id"], json.dumps(service_list), requested_date_time, slot_id, message)
            if Slot.book(session["user_id"], requested_slot, new_appointment):
                return render_template("message_page.html", message_title="success", 
                                                        message_header="You requested appointment on", 
                                                        message_text= " " + requested_date.strftime("%m/%d/%Y") + " at " + requested_time.strftime("%H:%M") + ". We will send you a confirmation.", 
                                                        message_link="/", 
                                                        message_link_text="Home page.")
            else:
                return  render_template("apology.html", error_message="Something went wrong")
        
        # except Exception as er:
        #     print("##/book/ -- db query")
        #     print(er)
        #     return  render_template("apology.html", error_message="Something went wrong.")        

    else:
        return redirect("/")
