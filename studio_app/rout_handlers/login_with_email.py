from flask import flash, redirect, render_template, request, session
from ..services.user_service import UserService
from wtforms import ValidationError    
from ..validations.forms.login_forms import LoginByEmailForm

def login_with_email():     
    form = LoginByEmailForm()

    if request.method == "GET":
        return render_template("login_by_mail.html", form=form)

    try:
        if form.validate_on_submit():
            user_service = UserService()
            user_service.login_by_email_and_remember(form.email.data, form.do_remember_me.data)

            flash('logged in successfully')
            return redirect("/login-with-email/")

        else:
            flash('wrong login or password password')
            return redirect("/login-with-email/")

    except ValidationError as e:
            flash(str(e))
            return redirect("/login-with-email/")