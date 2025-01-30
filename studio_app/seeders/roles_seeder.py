from ..models.role import Role
from ..models.base import db

def seed_roles():
    roles = [
        Role(name="admin"),
        Role(name="client"),
        Role(name="tester")
    ]
    
    for role in roles:
        existing = Role.query.filter_by(name=role.name).first()
        if not existing:
            db.session.add(role)
    
    db.session.commit()