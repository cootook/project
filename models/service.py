import datetime
from flask_security import hash_password
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..studio_app.config import Config
from .base import db_base


class ServiceModel(db_base.Model):
    __tablename__ = "service"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")
    deleted: Mapped[bool] = mapped_column(default = False)

    def create(self, name, description):
        new_service = ServiceModel(name=name, description=description)
        db_base.session.add(new_service)
        db_base.session.commit()
        return new_service
    
    def delete(self):
        db_base.session.execute(update(ServiceModel).where(ServiceModel.id == self.id).values(deleted = True))
        db_base.session.commit()
        return
    
    @staticmethod
    def get_list_of_services_from_dict(data: dict):
        services = []
        for item in data:
            if item == data[item]:
                service = db_base.session.scalar(select(ServiceModel).where(ServiceModel.name == item, ServiceModel.deleted == False))
                if not service is None:
                    services.append(item)
        return services
