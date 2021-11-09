from abc import ABCMeta, abstractmethod

class GrantsService(metaclass=ABCMeta):
    @abstractmethod
    def verify(self):
        pass

    @abstractmethod
    def generate_token(self):
        pass
