import datetime
import json
import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from sqlalchemy.orm import Session as sqla_session
from sqlalchemy import select
from studio_app.db_classes import Appointment, Service, User, db_base
from ..helpers import get_js_object

def all_appointments():
    today = datetime.datetime.now()
    user_appointments_for_frontend = []
    user_appoint_db_v2 = Appointment.query.filter(Appointment.at >= today).order_by(Appointment.at).all()

    for aptmt in user_appoint_db_v2:
        tmp = aptmt.__dict__
        tmp.pop('_sa_instance_state', None)
        # print(tmp, "@@@")
        service = Service.query.filter(Service.id == Appointment.service_id).first()
        tmp["service_name"] = service.name
        tmp["service_description"] = service.description
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
    


    # except Exception as er:
    #     con.close()
    #     print("##/all_appointments/ --db connection")
    #     print(er)
    #     return  render_template("apology.html", error_message="Something went wrong")
         
    return render_template("all_appointments.html", user_appointments_for_frontend=user_appointments_for_frontend, user_appointments_for_template=user_appointments_for_template)

