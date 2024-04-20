from flask_security import ConfirmRegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ExtendedRegisterForm(ConfirmRegisterForm):
    name = StringField('Name', [DataRequired()])
    instagram = StringField('Instagram', [DataRequired()])
    tel = StringField('Phone number', [DataRequired()])