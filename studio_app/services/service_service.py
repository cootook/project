from typing import Tuple, List, Dict
from sqlalchemy.exc import SQLAlchemyError
from ..repositories.service_repository import ServiceRepository
from datetime import datetime
from ..models.service import ServiceModel

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
        try:
            if not name or not description:
                return False, "Service name and description are required"
                
            if self.service_repo.does_exist_and_active(name):
                return False, "This service already exists"
                
            self.service_repo.create(name, description)
            return True, ""
            
        except ValueError as e:
            return False, str(e)
        except SQLAlchemyError as e:
            print(f"ERROR {datetime.now()}: ServiceService.create_service: SQLAlchemy: {e}")
            return False, "Database error occurred"
        except Exception as e:
            print(f"ERROR {datetime.now()}: ServiceService.create_service: Exception: {e}")
            return False, "An unexpected error occurred"
    
    def get_active_services(self) -> List[Dict]:
        try:
            return self.service_repo.get_list_of_dict_of_active_services()
        except SQLAlchemyError:
            print(f"ERROR {datetime.now()}: ServiceService.get_active_services: SQLAlchemy")
            return []
        
    def delete_by_id(self, id: int) -> bool:
        try:
            service = self.service_repo.get_by_id(id)
            if service is None:
                return False
            success = self.service_repo.delete_soft(service)
            return success
        except Exception as e:
            print(f"ERROR {datetime.now()}: Failed to delete service ID {id}")
            return False
        
    def get_by_id_as_dict(self, id: int) -> dict | None:
        try:
            service = self.service_repo.get_by_id()
            if service is None:
                return None
            return service.__dict__
        except Exception as e:
            print(f"ERROR {datetime.now()}: Failed to get service ID {id} as dict")
            return None
        
    def edit_by_id(self, id: int, name: str, description: str) -> bool:
        try:
            service = self.service_repo.get_by_id(id)
            if service is None:
                return False
            success = self.service_repo.update(service, name, description)
            return success
        except Exception as e:
            print(f"ERROR {datetime.now()}: Failed to update service ID {id}")
            return False
        
    def does_exist_by_id(self, id: int) -> bool:
        try:
            service = self.service_repo.get_by_id(id)
            if service is None:
                return False
            return True
        except Exception as e:
            print(f"ERROR {datetime.now()}: Failed to update service ID {id}")
            raise