from sqlalchemy import select
from ..models.service import ServiceModel
from ..repositories.service_repository import ServiceRepository

class ServiceService():
    def __init__(self):
        self.service_repo = ServiceRepository()

    def get_list_of_services_from_form_data_dict(self, data: dict):
        services = []
        for item in data:
            if item == data[item]:
                if self.service_repo.does_exist_and_active(item):
                    services.append(item)
        return services