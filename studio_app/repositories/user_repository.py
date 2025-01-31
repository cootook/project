from ..webapp import user_datastore

class UserRepository:
    @staticmethod
    def create_user(**kwargs: any):
        return user_datastore.create_user(**kwargs)
