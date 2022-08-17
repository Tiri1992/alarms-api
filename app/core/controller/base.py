"""Controller interface"""

from abc import ABC
from abc import abstractmethod


class CrudController(ABC):

    @abstractmethod
    def create(self, schema):
        pass 

    @abstractmethod
    def get(self):
        pass 

    @abstractmethod
    def update(self, schema, id):
        pass 

    @abstractmethod
    def delete(self, id):
        pass 

class CheckController(ABC):

    @abstractmethod
    def exists(self):
        pass

    
