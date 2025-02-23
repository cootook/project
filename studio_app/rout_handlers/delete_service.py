from flask import redirect, render_template, request, Response
from ..services.service_service import ServiceService
from ..error_handlers.error_handlers import ErrorHandler
from http import HTTPStatus
from typing import Dict, Tuple, Union
from flask_security import csrf_token_required

error_handler = ErrorHandler()
service_service = ServiceService()

def delete_service() -> Tuple[Union[Response, str], int]:
    if request.method == "POST":
        try:
            return  _handle_delete_post()        
        except Exception as e:
            return error_handler.handle_error(
                error_point="/delete_service/",
                message="Failed to delete service",
                status_code=HTTPStatus.BAD_REQUEST
            )
           
    else:
        try:
            service_id = _extract_form_data_get()
            service = service_service.get_by_id_as_dict(service_id)
            return render_template("delete_service.html", service=service), HTTPStatus.OK
        except Exception as e:
            return error_handler.handle_error(
                error_point="/delete_service/",
                message=f"Failed to find service by ID {service_id} to delete",
                status_code=HTTPStatus.BAD_REQUEST
            )        
        
@csrf_token_required
def _handle_delete_post() -> Tuple[Union[Response, str], int]:
    try:
        data = _extract_form_data_post()
        return _process_deleting(data)
    except ValueError as e:
        return error_handler.handle_error(
            error_point="/delete_service/",
            message=str(e),
            status_code=HTTPStatus.BAD_REQUEST
        )
    
def _extract_form_data_post() -> Dict[str, int]:
    try:
        service_id = request.form.get("service_id")
        if service_id is None:
            raise ValueError("service_id is missing from form data")
        return {
            'service_id': int(service_id)
        }
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse form data: {str(e)}")
    
def _extract_form_data_get() -> int:
    try:
        service_id = request.args.get("service_id_delete")
        if service_id is None:
            raise ValueError("service_id_delete is missing from query parameters")
        return int(service_id)
        
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to parse form data: {str(e)}")

def _process_deleting(data: Dict[str, int]) -> Tuple[Union[Response, str], int]:
    service_service.delete_by_id(data['service_id'])
    print(f"Successfully deleted service ID {data['service_id']}")
    return redirect("/add_service/"), HTTPStatus.OK
 