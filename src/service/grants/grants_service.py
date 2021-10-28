from abc import ABCMeta, abstractmethod

class GrantsService(metaclass=ABCMeta):
    EXPIRE_IN = 3600
    
    def setModel(self, model):
        self.model = model

    @abstractmethod
    def validation(self):
        pass

    @abstractmethod
    def generate_token(self):
        pass
