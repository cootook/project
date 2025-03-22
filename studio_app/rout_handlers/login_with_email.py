from flask import flash, redirect, render_template, request, session
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository
from wtforms import ValidationError    
from ..validations.forms.login_forms import LoginByEmailForm

def login_with_email():     
    form = LoginByEmailForm()

    if request.method == "GET":
        return render_template("login_by_mail.html", form=form)

    try:
        if form.validate_on_submit():
            user_service = UserService()
            user_repo = UserRepository()
            user_service.login_by_email_and_remember(form.email.data, form.do_remember_me.data)

            # legacy: backward compatibility
            user_to_login = user_repo.get_user_by_email(form.email.data)
            session["user_id"] = user_to_login.__dict__["id"]
            session["is_admin"] = 1 if user_to_login.has_role("admin") else 0            
            session["name"] = user_to_login.__dict__["name"]
            session["login"] = user_to_login.__dict__["email"]
            session["tell"] = user_to_login.__dict__["us_phone_number"]

            flash('logged in successfully')
            return redirect("/login-with-email/")

        else:
            flash('wrong login or password password')
            return redirect("/login-with-email/")

    except ValidationError as e:
            flash(str(e))
            return redirect("/login-with-email/")