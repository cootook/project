from studio_app.db_classes import db_base, Service
from sqlalchemy import select, update
from flask import redirect, render_template, request


def edit_service():
    if request.method == "POST":
        service_id = request.form.get("service_id")
        service_name = request.form.get("service")
        service_description = request.form.get("description")

        print("#new", service_id, service_name, service_description)

        db_base.session.execute(update(Service).where(Service.id == service_id).values(name = service_name, description = service_description))
        db_base.session.commit()
        
        return redirect("/add_service/")
            
    else:
        service_id = int(request.args['service_id_edit'])   
        print(service_id)
        service_edit = db_base.session.scalar(select(Service).where(Service.id == service_id))
        print(service_edit.__dict__["name"], service_edit.__dict__["description"])


        return render_template("edit_service.html", service_edit = service_edit)
    
    
 