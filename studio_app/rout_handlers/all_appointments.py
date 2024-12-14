import datetime
import json

from flask import flash, redirect, render_template, request, session
from sqlalchemy import select
from studio_app.db_classes import Appointment, User, db_base
from ..helpers import get_js_object

def all_appointments():
    today = datetime.datetime.now()
    user_appointments_for_frontend = []
    user_appoint_db_v2 = Appointment.query.order_by(Appointment.at).all()

    for aptmt in user_appoint_db_v2:
        tmp = aptmt.__dict__
        tmp.pop('_sa_instance_state', None)
        tmp["service"] = json.loads(tmp["service"])
        user_appointments_for_frontend.append(tmp)
        client = User.query.filter(User.id == Appointment.user_id).first()
        if not client == None:
            tmp["client_name"] = client.name
            tmp["client_tel"] = client.tel 
            tmp["client_description"] = client.internal_description
        else:
            tmp["client_name"] = "no name"
            tmp["client_tel"] = "no telephone" 
            tmp["client_description"] = "-"
    user_appointments_for_template = user_appointments_for_frontend    
    user_appointments_for_frontend = get_js_object(user_appointments_for_frontend)
    
    return render_template("all_appointments.html", user_appointments_for_frontend=user_appointments_for_frontend, user_appointments_for_template=user_appointments_for_template)
