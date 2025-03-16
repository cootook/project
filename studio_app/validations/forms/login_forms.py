from flask_wtf import RecaptchaField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.simple import BooleanField, EmailField, PasswordField
from wtforms import ValidationError
from .base import BaseForm
from ...repositories.user_repository import UserRepository

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
    user = user_repo.get_user_by_email(form.login.data)
    
    if not user_repo.verify_and_update_password(user, field.data):
        raise ValidationError("wrong login or password")
      
class LoginByEmailForm(BaseForm):
    email = EmailField(
        'email', 
        validators=[
            DataRequired(message="email is required"),
            Length(min=2, max=100, message="email must be between 2 and 100 characters"),
            _login_validator
        ],
        name="login",
        id="login"
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
        validators=[
            DataRequired(message="remember check box")
        ],
        name="remember",
        id="remember"
    )

    token = RecaptchaField()
