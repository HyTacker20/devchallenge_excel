from abc import ABC


class RepositoryInterface(ABC):
    def get_instance(self, *args, **kwargs):
        pass

    def create_instance(self, *args, **kwargs):
        pass

    def update_instance(self, *args, **kwargs):
        pass

    def is_exist(self, *args, **kwargs):
        pass
