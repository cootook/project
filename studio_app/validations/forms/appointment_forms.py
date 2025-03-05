import datetime
from flask_wtf import RecaptchaField
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.fields.simple import TelField, HiddenField, BooleanField
from wtforms import ValidationError, SelectField
from .base import BaseForm
from ...services.phone_service import PhoneNumberService
from ...repositories.slot_repository import SlotRepository
from ...repositories.user_repository import UserRepository
from ...repositories.appointment_repository import AppointmentRepository

appointment_repo = AppointmentRepository()
slot_repo = SlotRepository()
user_repo = UserRepository()

def _phone_number_validator(
        form,
        field,

):
    phone_number_service = PhoneNumberService(field.data)
    if not phone_number_service.is_valid:
        raise ValidationError("phone number is not valid")
    
def _terms_and_privacy_concern_validator(
        form,
        field,
):
    """
    Custom validator for terms and privacy:
    """
    if not field.data:
        raise ValidationError("terms are not accepted")
    
def _slot_exists(
        form,
        field
):
    if slot_repo.get_by_id(int(field.data)) is None:
        raise ValidationError("no slot found")

def _date_in_form_and_slot_match(
        form,
        field
):
    date_time_pythonic = datetime.datetime.strptime(
            form.date_time_iso.data, 
            '%Y-%m-%dT%H:%M'
            ) 
    slot = slot_repo.get_by_id(int(field.data))
    if date_time_pythonic != slot.date:
        raise ValidationError("Error: date and slot do not match")

def _appointment_in_form_belongs_to_user(
        form,
        field
):
    appointment_id = int(form.appointment_id.data)
    appointment = appointment_repo.get_by_id(appointment_id)
    if appointment.user_id != int(field.data):
        raise ValidationError("Error: appointment does not belong to user")

def _user_exists(
        form,
        field
):
    if not user_repo.does_user_exist_by_id(int(field.data)):
        raise ValidationError("Error: user does not exist")
    
class BaseAppointmentForm(BaseForm):
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters")
        ],
        name="client_name",
        id="client_name"
        )
    date_time_iso = DateTimeLocalField(
        'Date and time', 
        format="%Y-%m-%dT%H:%M", 
        validators=[
            DataRequired(message="Date and time are required"),
            Length(min=16, max=16, message="Wrong format")
            ],
        name="datetime-iso",
        id="datetime-iso"
        )   
    message = StringField('Message', validators=[
        DataRequired(message="Message is required"),
        Length(min=2, max=300, message="Name must be between 2 and 100 characters")
        ],
        name="message-text",
        id="message-text"
        )
 
class BookAppointmentForm(BaseAppointmentForm):
    slot_id = HiddenField(
        validators=[
            DataRequired(),
            _slot_exists,
            _date_in_form_and_slot_match
        ],
        name="slot_id",
        id="slot_id"
    )
    phone= TelField('Phone number', validators=[
        DataRequired(message="Phone number is required"),
        Length(min=10, max=14, message="Service name must be between 2 and 100 characters"),
        _phone_number_validator
        ],
        name="full_phone",
        id="full_phone"
        )
    token = RecaptchaField()
    terms_and_privacy_concern = BooleanField("Terms and privacy", validators=[
        DataRequired(),
        _terms_and_privacy_concern_validator
        ],
        name="client_name",
        id="client_name"
        )
    

class EditAppointmentForm(BaseAppointmentForm):
    appointment_id = HiddenField(validators=[
        DataRequired(),
        Length(min=1, max=6),
        _user_exists,
        _appointment_in_form_belongs_to_user
        ],
        name="appointment_id",
        id="appointment_id"
        )
    user_id = HiddenField(validators=[
        DataRequired(),
        Length(min=1, max=4),
        _user_exists,
        _appointment_in_form_belongs_to_user
        ],
        name="user_id",
        id="user_id"
        )
    duration = IntegerField('Duration of the appointment', 
        name="new_duration",
        id="new_duration"
        )