import datetime

from flask import redirect, render_template, request, session
from ..helpers import validate_recaptcha
from studio_app.db_classes import Appointment, Slot, db_base

def book():
    
    if request.method == "POST":
        try:                  
            token = request.form.get("g-recaptcha-response")
            minute = int(request.form.get("minute"))
            hour = int(request.form.get("hour"))
            day = int(request.form.get("date"))
            month = int(request.form.get("month")) + 1 # in calendar.js month range starts from 0
            year = int(request.form.get("year"))
            slot_id = int(request.form.get("slot_id"))
            manicure = True if request.form.get("manicure") is not None else False
            pedicure = True if request.form.get("pedicure") is not None else False
            message = request.form.get("message-text")            

        except Exception as er:
            print("##/book/ --request.form.get")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong") 

        if not validate_recaptcha(token):
            return  render_template("apology.html", error_message="Sorry. Something went wrong with anti robot, maybe reCaptcha that you have just checked expired. Please, try arain.")

        requested_date = datetime.date(year, month, day)
        requested_time = datetime.time(hour, minute)
        requested_date_time = datetime.datetime(year, month, day, hour, minute)
        
        try:
            requested_slot = Slot.query.filter(Slot.id == slot_id, Slot.date == requested_date, Slot.time == requested_time).first()          
            if not requested_slot.opened:
                return  render_template("apology.html", error_message="Time is not available")
            else:
                # define service 
                requested_service = "combo" if manicure and pedicure else "manicure" if manicure else "pedicure"
                new_appointment = Appointment.create(session["user_id"], requested_service, requested_date_time, slot_id, message)
                if Slot.book(session["user_id"], requested_slot, new_appointment):
                    return render_template("message_page.html", message_title="success", 
                                                            message_header="You requested appointment on", 
                                                            message_text= " " + requested_date.strftime("%m/%d/%Y") + " at " + requested_time.strftime("%H:%M") + ". We will send you a confirmation.", 
                                                            message_link="/", 
                                                            message_link_text="Home page.")
                else:
                    return  render_template("apology.html", error_message="Something went wrong")
        
        except Exception as er:
            print("##/book/ -- db query")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong")        

    else:
        return redirect("/")
