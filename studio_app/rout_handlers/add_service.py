from studio_app.db_classes import db_base, Service
from sqlalchemy import select
from flask import redirect, render_template, request


def add_service():
    services_bd = db_base.session.scalars(select(Service)).fetchall()
    services_list = []
    for service in services_bd:
        service = service.__dict__
        services_list.append(service)

    if request.method == "POST":
        service_name = request.form.get("service")
        service_description = request.form.get("description")
        if service_name == None or service_description == None or service_name == "" or service_description == "":
            return render_template("apology.html", error_message="service name and description cannot be empty")
        for service in services_list:
            if service["name"].lower() == service_name.lower():
                return render_template("apology.html", error_message="this service already exist")
        new_service_db = Service(name = service_name, description = service_description)
        db_base.session.add(new_service_db)
        db_base.session.commit()
        
        return redirect("/add_service/")
            
    else:
        return render_template("add_service.html", services_list=services_list)
    
 