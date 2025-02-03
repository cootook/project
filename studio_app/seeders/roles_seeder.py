from ..models.role import RoleModel
from ..models.base import db_base

def seed_roles():
    roles = [
        RoleModel(name="admin"),
        RoleModel(name="client"),
        RoleModel(name="tester")
    ]
    
    for role in roles:
        existing = RoleModel.query.filter_by(name=role.name).first()
        if not existing:
            db_base.session.add(role)
    
    db_base.session.commit()