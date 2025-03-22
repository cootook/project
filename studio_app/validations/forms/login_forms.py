from flask_wtf import RecaptchaField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.simple import BooleanField, EmailField, PasswordField
from wtforms import ValidationError
from .base import BaseForm
from ...repositories.user_repository import UserRepository

DATA_CALLBACK_JS_FUNC_NAME = "set_is_recaptcha_true"
DATA_EXPIRED_CALLBACK_JS_FUNC_NAME = "set_is_recaptcha_false"

user_repo = UserRepository()

def _login_validator(
        form,
        field
):
    if not user_repo.does_user_exist_by_email(field.data):
        raise ValidationError("wrong login or password")
    
def _password_validator(
        form,
        field
):
    try:
        password_ok = user_repo.verify_and_update_password(
            user_repo.get_user_by_email(form.email.data),
            field.data)
    except:
        password_ok = False
    
    if not password_ok:
        raise ValidationError("wrong login or password")
      
class LoginByEmailForm(BaseForm):
    email = EmailField(
        'email', 
        validators=[
            DataRequired(message="email is required"),
            Length(min=2, max=100, message="email must be between 2 and 100 characters")
        ],
        name="email",
        id="email"
        )
    
    password = PasswordField(
        'password',
        validators=[
            DataRequired(message="password is required"),
            _password_validator
        ],
        name="password",
        id="password"
    )

    do_remember_me = BooleanField(
        'remember me',
        name="remember",
        id="remember", 
        default=False    
    )

    recaptcha = RecaptchaField()
