from flask import redirect, render_template, request, session
from ..services.booking import Booking
from ..services.verification import SmsVerificationOfBooking

def confirm_phone():    
    if request.method == "POST":
        try:                  
            code = request.form.get("code")                    
        except Exception as er:
            print("##/confirm-phone/ --request.form.get")
            print(er)
            return  render_template("apology.html", error_message="Something went wrong") 
        
        booking = Booking.from_json(session["booking_json"])
        verification = SmsVerificationOfBooking(booking)
        is_code_ok = verification.verify_code(code)
        if not is_code_ok:
                return render_template(
                    "booking_sms_confirmation_code.html", 
                    phone=booking.client_phone,
                    name=booking.client_name
                    )
        elif is_code_ok:
            booking.reserve_slot()
            return render_template("message_page.html", message_title="success", 
                                        message_header="You requested appointment on", 
                                        message_text= f"""  {booking.date.strftime("%m/%d/%Y")} at {booking.time.strftime("%H:%M")}.
                                          We will review the request and contact you as soon as possible.""", 
                                        message_link="/", 
                                        message_link_text="Home page.")
    else:
        return redirect("/")