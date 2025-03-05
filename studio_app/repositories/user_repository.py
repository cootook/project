from flask_security import hash_password
from sqlalchemy import select, update
from ..models.user import UserModel
from ..models.role import RoleModel
from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    def create_user(self, **kwargs) -> UserModel | None:
        """
        to create new user using input phone use
        get_or_create_and_update_user_by_phone()

        returns None if user with passed email or phone already exists
        """
        if 'email' in kwargs and self.does_user_exist_by_email(kwargs['email']):
            print(f'UserRepository: user with email {kwargs["email"]} already exists')
            return None
            
        if 'tel' in kwargs and self.does_user_exist_by_tel(kwargs['tel']):
            print(f'UserRepository: user with phone {kwargs["tel"]} already exists')
            return None

        new_user = self.user_store.create_user(**kwargs)
        self.db.add(new_user)
        self.db.commit()
        return new_user

    def add_role_to_user(self, user: UserModel, role: str | RoleModel) -> bool:
        """
        Adds a role to a user.
        
        Args:
            user: The user to manipulate
            role: The role to add to the user. Can be a Role object or string role name
        Returns:
            True if role was added, False if role already existed
        """
        return self.user_store.add_role_to_user(user, role)

    def does_user_exist_by_email(self, email: str) -> bool:
        user = self.db.scalar(
            select(UserModel).where(UserModel.email == email)
        )
        return user is not None
    
    def does_user_exist_by_id(self, id: int) -> bool:
        user = self.db.scalar(
            select(UserModel).where(UserModel.id == id)
        )
        return user is not None

    def does_user_exist_by_tel(self, tel: str) -> bool:
        user = self.db.scalar(
            select(UserModel).where(UserModel.tel == tel)
        )
        return user is not None

    def get_user_by_email(self, email: str) -> UserModel | None:
        return self.db.scalar(
            select(UserModel).where(UserModel.email == email)
        )

    def get_user_by_tel(self, tel: str) -> UserModel | None:
        return self.db.scalar(
            select(UserModel).where(UserModel.tel == tel)
        )
    
    def get_user_by_id(self, id) -> UserModel | None:
        return self.db.scalar(
            select(UserModel).where(UserModel.id == id)
        )

    def get_or_create_and_update_user_by_phone(self, phone: str) -> UserModel:
        default_user_data = {
            'email': f"{phone}@{self.config.MAIL_DEFAULT_DOMAIN}",
            'password': hash_password(self.config.DEFAULT_PASSWORD)
        }
                
        user_exists_by_email = self.does_user_exist_by_email(default_user_data['email'])
        user_exists_by_phone = self.does_user_exist_by_tel(phone)
        


        if not user_exists_by_phone and not user_exists_by_email:
            return self.create_user(
                tel=phone,
                **default_user_data
            )
        
        if not user_exists_by_phone:
            user = self.get_user_by_email(default_user_data['email'])
            return self.update_user_data(
                user,
                tel=phone
            )
            
        user = self.get_user_by_tel(phone)
        return self.update_user_data(
            user,
            **default_user_data
        )

    def update_user_data(self, user: UserModel, **kwargs: any) -> UserModel:
        self.db.execute(
            update(UserModel).where(UserModel.id == user.id).values(**kwargs)
        )
        self.db.commit()
        return user
