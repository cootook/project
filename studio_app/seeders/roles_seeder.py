from ..models.role import RoleModel
from ..models.base import data_base
from flask_sqlalchemy import SQLAlchemy


def seed_roles(db_session: SQLAlchemy=data_base):
    roles = [
        RoleModel(name="admin"),
        RoleModel(name="client"),
        RoleModel(name="tester")
    ]
    
    for role in roles:
        existing = RoleModel.query.filter_by(name=role.name).first()
        if not existing:
            db_session.session.add(role)
    
    db_session.session.commit()