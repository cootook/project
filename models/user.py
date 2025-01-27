import datetime
from flask_security import hash_password
from flask_security.models import fsqla_v3 as fsqla
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..studio_app.config import Config
from .base import db_base


class UserModel(db_base.Model, fsqla.FsUserMixin):
    _tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(unique = True)
    password: Mapped[Optional[str]]
    active: Mapped[str] = mapped_column(default = True)
    confirmed_at: Mapped[Optional[datetime.datetime]]
    last_login_at: Mapped[Optional[datetime.datetime]]
    current_login_at: Mapped[Optional[datetime.datetime]]
    last_login_ip: Mapped[Optional[str]] 
    current_login_ip: Mapped[Optional[str]] 
    login_count: Mapped[int] 
    name: Mapped[Optional[str]]   
    tel: Mapped[Optional[str]]
    internal_description: Mapped[Optional[str]]  
    lust_update_at: Mapped[Optional[datetime.datetime]] 
    lust_update_by_id = mapped_column(ForeignKey("user.id"), nullable=True)
    deleted: Mapped[bool] = mapped_column(default = False)
    deleted_at: Mapped[Optional[datetime.datetime]]
    deleted_by_id = mapped_column(ForeignKey("user.id"), nullable=True)

    @staticmethod
    def get_or_create_id_by_phone(phone: str, name: str):
        """
        the method updates user's name if user with this phone exists
        """
        user = db_base.session.scalar(select(UserModel).where(UserModel.tel == phone))
        from studio_app.webapp import user_datastore
        if user is None:
            user = user_datastore.create_user(
                tel = phone, 
                name = name, 
                email = f"{phone}@{Config.MAIL_DEFAULT_DOMAIN}", 
                password = hash_password(Config.DEFAULT_PASSWORD))
            db_base.session.add(user)
            db_base.session.commit()
            user_datastore.add_role_to_user(user, "client")
        else:
            db_base.session.execute(update(UserModel).where(UserModel.tel == phone).values(name = name))
            user_datastore.add_role_to_user(user, "client")
            db_base.session.commit()
        return user.id
    
    @staticmethod
    def get_user_by_id(id):
        return db_base.session.scalar(select(UserModel).where(UserModel.id == id))
