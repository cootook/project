from http import HTTPStatus
from .error_handlers import ErrorHandler
from typing import Tuple, Dict, Any

class AppointmentErrorHandler(ErrorHandler):
    def __init__(self):
        super().__init__(
            template="apology.html",  
            default_message="Unable to process appointment request",
            default_status=HTTPStatus.BAD_REQUEST
        )
    
    def handle_appointment_error(
        self, 
        error: Exception, 
        appointment_id: str = None,
        additional_data: Dict[str, Any] = None
    ) -> Tuple[str, int]:
        context = {}
        if appointment_id:
            context['appointment_id'] = appointment_id
        if additional_data:
            context.update(additional_data)
            
        if isinstance(error, ValueError):
            return self.handle_error(
                error_point="/appointment",
                message=f"Invalid appointment data: {str(error)}",
                status_code=HTTPStatus.BAD_REQUEST,
                additional_context=context
            )
        
        return self.handle_error(
            error_point="/appointment",
            message=f"Appointment processing error: {str(error)}",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            additional_context=context
        )