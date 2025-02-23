from flask import redirect, render_template, request, Response
from ..services.service_service import ServiceService
from ..error_handlers.error_handlers import ErrorHandler
from http import HTTPStatus
from typing import Dict, Tuple, Union
from flask_security import csrf_token_required

error_handler = ErrorHandler()
service_service = ServiceService()


def edit_service() -> Tuple[Union[Response, str], int]:
    if request.method == "POST":
        try:
            return  _handle_edit_post()        
        except Exception as e:
            return error_handler.handle_error(
                error_point="/edit_service/",
                message="Failed to edit service",
                status_code=HTTPStatus.BAD_REQUEST
            )
           
    else:
        try:
            service_id = _extract_form_data_get()
            service = service_service.get_by_id_as_dict(service_id)
            return render_template("edit_service.html", service_edit = service.__dict__), HTTPStatus.OK
        except Exception as e:
            return error_handler.handle_error(
                error_point="/edit_service/",
                message=f"Failed to find service by ID {service_id} to edit",
                status_code=HTTPStatus.BAD_REQUEST
            )    
    
@csrf_token_required
def _handle_edit_post() -> Tuple[Union[Response, str], int]:
    try:
        data = _extract_form_data_post()
        return _process_editing(data)
    except ValueError as e:
        return error_handler.handle_error(
            error_point="/edit_service/",
            message=str(e),
            status_code=HTTPStatus.BAD_REQUEST
        )
    
def _extract_form_data_post() -> Dict[str, Union[int, str]]:
    try:
        service_id = request.form.get("service_id")
        service_name = request.form.get("service")
        service_description = request.form.get("description")
        if service_id is None or service_id.strip() == '':
            raise ValueError("service_id is missing from form data")
        if service_name is None or service_name.strip() == '':
            raise ValueError("service_name is missing from form data")
        if service_description is None or service_description.strip() == '':
            raise ValueError("service_description is missing from form data")
        
        try:
            service_id_int = int(service_id)
            if service_id_int <= 0:
                raise ValueError("Service ID must be a positive number")
        except ValueError:
            raise ValueError("Invalid service ID format")
        
        return {
            'service_id': service_id_int,
            'service_name': str(service_name),
            'service_description': str(service_description)
        }
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse form data: {str(e)}")
    
def _extract_form_data_get() -> int:
    try:
        service_id = request.args.get("service_id_edit")
        if service_id is None:
            raise ValueError("service_id_edit is missing from query parameters")
        
        service_id_int = int(service_id)
        if service_id_int <= 0:
            raise ValueError("service_id must be a positive integer")
            
        return service_id_int
        
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse form data: {str(e)}")

def _process_editing(data: Dict[str, Union[int, str]]) -> Tuple[Union[Response, str], int]:
    does_exist = service_service.does_exist_by_id(data["service_id"])
    if not does_exist:
        return error_handler.handle_error(
                error_point="/edit_service/",
                message=f"Service with ID {data['service_id']} not found",
                status_code=HTTPStatus.NOT_FOUND
            )
    
    service_service.edit_by_id(
        id=data["service_id"],
        name=data["service_name"],
        description=data["service_description"]
    )

    print(f"Successfully edited service ID {data['service_id']}")

    return redirect("/add_service/"), HTTPStatus.OK
 