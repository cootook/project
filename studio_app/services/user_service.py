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

        try:
            self.user = self.user_repo.get_user_by_id(id)
            return login_user(self.user)
        except Exception as e:
            self._log_error("Failed log in user by ID", e)
            return False
    
    def _log_error(self, message: str, exception: Exception = None) -> None:
        error_msg = f"Error: {message}"
        if exception:
            error_msg += f" - {str(exception)}"
        print(error_msg)