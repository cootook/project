from ..models.user import UserModel
from ..repositories.user_repository import UserRepository
from flask_security import login_user, logout_user

class UserService:
    def __init__(self, user: UserModel=None):
        self.user = user
        self.user_repo = UserRepository()    

    def login_by_id(self, id: int) -> bool:
        if self.user is not None:
            logout_user(self.user)

        self.user = self.user_repo.get_user_by_id(id)
        return login_user(self.user)
    
    def login_by_email_and_remember(self, email: str, remember: bool=None):
        if self.user is not None:
            logout_user(self.user)

        self.user = self.user_repo.get_user_by_email(email)
        return login_user(self.user, remember)
    