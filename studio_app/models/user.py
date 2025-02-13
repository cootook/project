import datetime
from flask_security import hash_password, SQLAlchemyUserDatastore
from flask_security.models import fsqla_v3 as fsqla
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..config import Config
from .base import data_base
from .role import RoleModel
from typing import List

class UserModel(data_base.Model, fsqla.FsUserMixin):
    __tablename__ = "user"
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
    last_update_at: Mapped[Optional[datetime.datetime]] 
    last_update_by_id = mapped_column(ForeignKey("user.id"), nullable=True)
    deleted: Mapped[bool] = mapped_column(default = False)
    deleted_at: Mapped[Optional[datetime.datetime]]
    deleted_by_id = mapped_column(ForeignKey("user.id"), nullable=True)
    roles: Mapped[List[RoleModel]] = relationship(
        "RoleModel",
        secondary="roles_users",
        backref=backref("users", lazy="dynamic")
        )
