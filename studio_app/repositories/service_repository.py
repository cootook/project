from sqlalchemy import select, update
from ..models.service import ServiceModel
from random import randrange
from .base_repository import BaseRepository


class ServiceRepository(BaseRepository):

    def create(self, name: str, description: str) -> ServiceModel:
        new_service = ServiceModel(name=name, description=description)
        self.db.add(new_service)
        self.db.commit()
        return new_service
    
    def delete(self):
        self.db.execute(update(ServiceModel).where(ServiceModel.id == self.id).values(deleted = True))
        self.db.commit()
        
    
    def update(self, service: ServiceModel, name: str, description: str=''):
        self.db.execute(update(ServiceModel).where(ServiceModel.id == service.id).values(name=name, description=description))
        self.db.commit()
        

    def does_exist_and_active(self, name: str) -> bool:
        service = self.db.scalar(select(ServiceModel).where(ServiceModel.name == name, ServiceModel.deleted == False))
        return False if service is None else True