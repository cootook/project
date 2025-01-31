from ..webapp import user_datastore, hash_password
from sqlalchemy import select, update
from ..webapp import db_base, UserModel, RoleModel
from ..config import Config

class UserRepository:
    @staticmethod
    def create_user(**kwargs)  -> UserModel:
        """
        returns None if user with passed email or phone already exists
        """
        if 'email' in kwargs:
            if UserRepository.does_user_exist_by_email(kwargs['email']):
                print(
                    f'UserRepository: user with email {kwargs["email"]} already exists'
                )
                return None
        elif 'tel' in kwargs:
            if UserRepository.does_user_exist_by_tel(kwargs['tel']):
                print(
                    f'UserRepository: user with phone {kwargs["tel"]} already exists'
                )
                return None
        new_user = user_datastore.create_user(**kwargs)
        db_base.session.add(new_user)
        db_base.session.commit()
        return new_user
    
    @staticmethod
    def add_role_to_user(user: UserModel, role: str | RoleModel) -> bool:
        """Adds a role to a user.

        :param user: The user to manipulate.
        :param role: The role to add to the user. Can be a Role object or
            string role name
        :return: True is role was added, False if role already existed.
        """
        return user_datastore.add_role_to_user(user, role)
    
    @staticmethod
    def does_user_exist_by_email(email: str) -> bool:
        user_by_email = db_base.session.scalar(
        select(UserModel).where(UserModel.email == email)
        )
        return False if user_by_email is None else True
    
    @staticmethod
    def does_user_exist_by_tel(tel: str) -> bool:
        user_by_tel = db_base.session.scalar(
        select(UserModel).where(UserModel.email == tel)
        )
        return False if user_by_tel is None else True
    
    @staticmethod
    def get_user_by_email(email: str) -> UserModel | None:
        return select(UserModel).where(UserModel.email == email)
    
    @staticmethod
    def get_user_by_tel(tel: str) -> UserModel | None:
        return select(UserModel).where(UserModel.tel == tel)
    
    @staticmethod
    def get_or_create_and_update_user_by_phone(phone: str) -> UserModel:
        default_email = f"{phone}@{Config.MAIL_DEFAULT_DOMAIN}"
        user_by_default_email = UserRepository.get_user_by_email(default_email)
        user_by_phone = UserRepository.get_or_create_id_by_phone(phone)
        if user_by_phone is None and user_by_default_email is None:
            return UserRepository.create_user(
                tel = phone, 
                email = default_email, 
                password = hash_password(Config.DEFAULT_PASSWORD)
            )
        elif user_by_phone is None:
            return UserRepository.update_user_data(
                user_by_default_email,
                tel = phone, 
                password = hash_password(Config.DEFAULT_PASSWORD) 
                )
        else:
            return UserRepository.update_user_data(
                user_by_phone,
                tel = phone, 
                email = default_email, 
                password = hash_password(Config.DEFAULT_PASSWORD) 
                )
    
    @staticmethod
    def update_user_data(user: UserModel, **kwargs: any) -> UserModel:
        db_base.session.execute(
            update(UserModel).where(UserModel.id == user.id).values(**kwargs)
            )
        db_base.session.commit()
