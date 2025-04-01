from ..models.user import UserModel
from ..repositories.user_repository import UserRepository
from flask import session
from flask_security import login_user, logout_user

def _set_legacy_session_param_for_logged_user(user, session):
    session["user_id"] = user.__dict__["id"]
    session["is_admin"] = 1 if user.has_role("admin") else 0            
    session["name"] = user.__dict__["name"]
    session["login"] = user.__dict__["email"]
    session["tell"] = user.__dict__["us_phone_number"]

class UserService:
    def __init__(self, user: UserModel=None):
        self.user = user
        self.user_repo = UserRepository()    

    def login_by_id(self, id: int) -> bool:
        if self.user is not None:
            logout_user(self.user)

        self.user = self.user_repo.get_user_by_id(id)
        login = login_user(self.user, True)

        if login:
            _set_legacy_session_param_for_logged_user(self.user, session)

        return login
    
    def login_by_email_and_remember(self, email: str, remember: bool=None):
        if self.user is not None:
            logout_user(self.user)

        self.user = self.user_repo.get_user_by_email(email)
        login = login_user(self.user, remember)
        
        if login:
            _set_legacy_session_param_for_logged_user(self.user, session)

        return login
    