from flask import render_template
from typing import Tuple, Callable, Optional
from datetime import datetime
import logging

class ErrorHandler:
    def __init__(
        self,
        template: str = "apology.html",
        default_message: str = "Unexpected error",
        default_status: int = 500,
        logger: Optional[Callable] = None
    ):
        self.template = template
        self.default_message = default_message
        self.default_status = default_status
        self.logger = logger or self._default_logger
        
        if logger is None:
            logging.basicConfig(
                format='%(asctime)s - %(levelname)s - %(message)s',
                level=logging.ERROR
            )
    
    def _default_logger(self, error_point: str, message: str, status_code: int) -> None:
        logging.error(f"{error_point} - {message} (Status: {status_code})")
    
    def handle_error(
        self,
        error_point: str,
        message: Optional[str] = None,
        status_code: Optional[int] = None,
        additional_context: dict = None
    ) -> Tuple[str, int]:

        message = message or self.default_message
        status_code = status_code or self.default_status
        
        self.logger(error_point, message, status_code)
        
        context = {"error_message": message}
        if additional_context:
            context.update(additional_context)
            
        return render_template(self.template, **context), status_code