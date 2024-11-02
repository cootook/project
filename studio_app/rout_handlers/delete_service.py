from studio_app.db_classes import db_base, Service
from sqlalchemy import select, delete
from flask import redirect, render_template, request


def delete_service():    

    if request.method == "POST":
        service_id = request.form.get("service_id")
        db_base.session.execute(delete(Service).where(Service.id == service_id))
        db_base.session.commit()        
        return redirect("/add_service/")
            
    else:
        service_id = request.args['service_id_delete']
        services_bd = db_base.session.scalars(select(Service).where(Service.id == service_id)).fetchall()
        services_list = []
        for service in services_bd:
            service = service.__dict__
            services_list.append(service)
        return render_template("delete_service.html", services_list=services_list)
    
 