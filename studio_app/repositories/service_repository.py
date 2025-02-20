from sqlalchemy import select, update
from ..models.service import ServiceModel
from random import randrange
from .base_repository import BaseRepository


class ServiceRepository(BaseRepository):

    def create(self, name: str, description: str) -> ServiceModel:
        if name == "" or description == "":
            raise ValueError("Name or description of service can not be empty.")
        new_service = ServiceModel(name=name, description=description)
        self.db.add(new_service)
        self.db.commit()
        return new_service
    
    def delete_soft(self, service: ServiceModel) -> bool:
        try:
            self.db.execute(update(ServiceModel).where(ServiceModel.id == service.id).values(deleted = True))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            self._log_error(f"Failed to set service as deleted: {service.id}", e)
            raise
        
    def get_by_id(self, id: int) -> ServiceModel | None:
        try:
            return self.db.scalar(select(ServiceModel).where(ServiceModel.id == id))
        except Exception as e:
            self._log_error(f"Failed to get service by ID: {id}", e)
            raise
    
    def update(self, service: ServiceModel, name: str, description: str='') -> bool:
        try:
            self.db.execute(update(ServiceModel).where(ServiceModel.id == service.id).values(name=name, description=description))
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            self._log_error(f"Failed to update service: {service.id}", e)
            raise        

    def does_exist_and_active(self, name: str) -> bool:
        service = self.db.scalar(select(ServiceModel).where(ServiceModel.name == name, ServiceModel.deleted == False))
        return False if service is None else True
    
    def get_list_of_dict_of_active_services(self) -> list:
        """
        returns
        [
            {
            id:, 
            name:, 
            description:
            }
        ]
        """
        services_bd = self.db.scalars(select(ServiceModel).where(ServiceModel.deleted == 0)).fetchall()
        services_list = []
        for service in services_bd:
            service = service.__dict__
            services_list.append(service)
        return services_list