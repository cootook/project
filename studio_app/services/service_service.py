from typing import Tuple, List, Dict
from ..repositories.service_repository import ServiceRepository

class ServiceService():
    def __init__(self):
        self.service_repo = ServiceRepository()

    def get_list_of_services_from_form_data_dict(self, data: dict) -> List[str]:
        services = []
        for item in data:
            if item == data[item]:
                if self.service_repo.does_exist_and_active(item):
                    services.append(item)
        return services
        
    def create_service(self, name: str, description: str) -> Tuple[bool, str]:
        if not name or not description:
            return False, "Service name and description are required"
            
        if self.service_repo.does_exist_and_active(name):
            return False, "This service already exists"
            
        self.service_repo.create(name, description)
        return True, ""
    
    def get_active_services(self) -> List[Dict]:
        """
        List[
            {
            id:, 
            name:, 
            description:
            },
        ]
        """
        return self.service_repo.get_list_of_dict_of_active_services()
    
    def get_list_of_active_services(self) -> List[str]:
        list_of_dict = self.service_repo.get_list_of_dict_of_active_services()
        list_of_str = []
        for service in list_of_dict:
            list_of_str.append(service["name"])
        return list_of_str
        
    def delete_by_id(self, id: int):
        service = self.service_repo.get_by_id(id)
        if service is None:
            raise
        self.service_repo.delete_soft(service)
        
    def get_by_id_as_dict(self, id: int) -> dict | None:
        service = self.service_repo.get_by_id(id)
        return None if service is None else service.__dict__
        
    def edit_by_id(self, id: int, name: str, description: str):
        service = self.service_repo.get_by_id(id)
        if service is None:
            raise
        self.service_repo.update(service, name, description)
        
    def does_exist_by_id(self, id: int) -> bool:
        service = self.service_repo.get_by_id(id)
        return False if service is None else True
