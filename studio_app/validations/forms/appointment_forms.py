import datetime
from flask_wtf import RecaptchaField
from flask import session
from flask_security import current_user
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.fields.simple import TelField, HiddenField, BooleanField
from wtforms.fields.numeric import DecimalField
from wtforms import ValidationError, SelectField
from wtforms.widgets import HiddenInput
from .base import BaseForm
from ...services.phone_service import PhoneNumberService
from ...repositories.slot_repository import SlotRepository
from ...repositories.user_repository import UserRepository
from ...repositories.appointment_repository import AppointmentRepository
from ...repositories.service_repository import ServiceRepository

appointment_repo = AppointmentRepository()
slot_repo = SlotRepository()
user_repo = UserRepository()
service_repo = ServiceRepository()

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
    
def _slot_is_open(
        form,
        field
):
    slot = slot_repo.get_by_id(field.data)
    if not slot.opened:
        raise ValidationError("slot is not available for booking")
    
def _date_in_form_and_slot_match(
        form,
        field
):
    if form.date_time_iso.data is None:
        raise ValidationError("Error: date missing")
    slot = slot_repo.get_by_id(int(field.data))
    if form.date_time_iso.data != datetime.datetime.combine(slot.date, slot.time):
        raise ValidationError("Error: date and slot do not match")

def _appointment_in_form_belongs_to_user(
        form,
        field
):
    appointment = appointment_repo.get_by_id(int(form.appointment_id.data))
    if appointment.user_id != int(field.data):
        raise ValidationError("Error: appointment does not belong to user")
    
def _appointment_exists(
        form,
        field
):
    if appointment_repo.get_by_id(int(field.data)) is None:
        raise ValidationError("Error: appointment does not exist")
    
def _appointment_belongs_to_user_id_in_session(
        form,
        field
):
    if not current_user.is_authenticated:
        raise ValidationError("no user for appointment")
    appointment = appointment_repo.get_by_id(int(field.data))
    if int(appointment.user_id) != int(current_user.id):
        raise ValidationError("Error: appointment does not belong to user")
    
def _code_matches_in_appointment(
        form,
        field
):
    if form.appointment_id is None:
        raise ValidationError("Error: appointment not found")
        
    appointment = appointment_repo.get_by_id(form.appointment_id.data)
    
    if int(appointment.sms_confirmation_code) != int(field.data):
        raise ValidationError("Error: wrong code")
    
def _user_exists(
        form,
        field
):
    if not user_repo.does_user_exist_by_id(int(field.data)):
        raise ValidationError("Error: user does not exist")
    
def _service_exists(
        form,
        field
):
    if not service_repo.does_exist_and_active(field.data):
        raise ValidationError("Error: wrong service")
    
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
            DataRequired(message="Date and time are required")
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
            _date_in_form_and_slot_match,
            _slot_is_open
        ],
        name="slot_id",
        id="slot_id"
    )
    full_phone = HiddenField(
        validators=[
            DataRequired(),
            _phone_number_validator
        ],
        name="full_phone",
        id="full_phone"
    )
    phone= TelField('Phone number', validators=[
        DataRequired(message="Phone number is required"),
        ],
        name="phone",
        id="phone"
        )
    token = RecaptchaField()
    terms_and_privacy_concern = BooleanField("Terms and privacy", validators=[
        DataRequired(message="You should accept terms"),
        _terms_and_privacy_concern_validator
        ],
        name="terms_and_privacy_concern",
        id="terms_and_privacy_concern",
        default=False
        )
    service = SelectField(
        "select service",
        validators=[
            DataRequired()
        ],
        name="service_selection",
        id="service_selection",
        validate_choice=False
    )
    

class EditAppointmentForm(BaseAppointmentForm):
    # not ready
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
    
class ConfirmAppointmentViaSms(BaseForm):
    appointment_id = IntegerField('appointment id', validators=[
        DataRequired(),
        _appointment_exists,
        _appointment_belongs_to_user_id_in_session
        ],
        name="appointment_id",
        id="appointment_id",
        widget=HiddenInput()
        )
    
    code = DecimalField('Code from text message', validators=[
        DataRequired(message="Code is required"),
        _code_matches_in_appointment
        ],
        places=4, 
        rounding=None, 
        use_locale=False, 
        number_format=None,
        name="code",
        id="code"
        )
