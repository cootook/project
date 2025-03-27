from ..services.service_service import ServiceService
from flask import redirect, render_template, request


def add_service():
    service_service = ServiceService()
    
    if request.method == "GET":
        services_list = service_service.get_active_services()
        return render_template("add_service.html", services_list=services_list)
    
    service_name = request.form.get("service", "").strip()
    service_description = request.form.get("description", "").strip()
    
    success, message = service_service.create_service(service_name, service_description)
    
    if not success:
        return render_template("apology.html", error_message=message)
        
    return redirect("/add_service/")
        