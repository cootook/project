from flask_wtf import FlaskForm
from wtforms import ValidationError


class BaseForm(FlaskForm):
    """Base form with common validation methods and utilities."""
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
            
    
    def log_validation_error(self, field_name, message):
        """Log validation error for debugging purposes."""
        print(f"Validation error in {self.__class__.__name__}.{field_name}: {message}")