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
    
    def delete_soft(self, service: ServiceModel):
        self.db.execute(update(ServiceModel).where(ServiceModel.id == service.id).values(deleted = True))
        self.db.commit()
        
    def get_by_id(self, id: int) -> ServiceModel | None:
        return self.db.scalar(select(ServiceModel).where(ServiceModel.id == id))

    
    def update(self, service: ServiceModel, name: str, description: str=''):
        self.db.execute(update(ServiceModel).where(ServiceModel.id == service.id).values(name=name, description=description))
        self.db.commit()
   
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
            temp_dict = {
                "id": service["id"],
                "name": service["name"],
                "description": service["description"]
            }
            services_list.append(temp_dict)
        return services_list
    
    def get_list_of_names_of_active_services(self) -> list:
        services_bd = self.db.scalars(
            select(ServiceModel)
            .where(ServiceModel.deleted == 0)).fetchall()
        list_of_names_of_active_services = []
        for service in services_bd:
            list_of_names_of_active_services.append(service.name)
        return list_of_names_of_active_services