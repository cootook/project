from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, ValidationError

from .base import BaseForm

class BaseAppointmentForm(BaseForm):
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters")
    ])
    date_time_iso = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters")
    ])   
    message   
        #     at = new_date_py,
        #     amount_time_min = new_duration,
        #     description = new_message + " | " + messages,
        #     service = dumps(new_service),
        #     last_update_at = datetime.datetime.now(),
        #     last_update_by_id = current_user.id
            # 'user_id': int(request.form.get("user_id_edit")),
            # 'booking_id': int(request.form.get("booking_id_edit")),
            # 'message': float(request.form.get("new_message", "")),
            # 'duration': int(request.form.get("new_duration")),
            # 'date_time': request.form.get("new_date"),
            # 'service': service_for_services.get_list_of_services_from_form_data_dict(request.form)

class CreateAppointmentForm(BaseAppointmentForm):
    phone= StringField('Service Name', validators=[
        DataRequired(message="Service name is required"),
        Length(min=2, max=100, message="Service name must be between 2 and 100 characters")
    ])
    token
    terms_and_privacy_concern
    

class EditAppointmentForm(BaseAppointmentForm):
    slot_id
    pass


class CreateServiceForm(BaseForm):
    """
    Form for validating new service creation.
    
    This form validates that the service name is unique and properly formatted
    before any data reaches the service layer.
    """
    service = StringField('Service Name', validators=[
        DataRequired(message="Service name is required"),
        Length(min=2, max=100, message="Service name must be between 2 and 100 characters")
    ])
    description = StringField('Description', validators=[
        DataRequired(message="Description is required"),
        Length(min=5, max=500, message="Description must be between 5 and 500 characters")
    ])
    
    def __init__(self, service_repository=None, *args, **kwargs):
        """
        Initialize form with optional service repository dependency.
        
        Args:
            service_repository: Repository used to check if service exists
            *args, **kwargs: Standard form arguments
        """
        super(CreateServiceForm, self).__init__(*args, **kwargs)
        self.service_repository = service_repository
    
    def validate_service(self, field):
        """
        Custom validator for service name uniqueness.
        
        This method is automatically called by WTForms during validation.
        It checks if a service with the same name already exists.
        
        Args:
            field: The form field being validated (service name)
            
        Raises:
            ValidationError: If service already exists
        """
        if self.service_repository and self.service_repository.does_exist_and_active(field.data):
            raise ValidationError("This service already exists")