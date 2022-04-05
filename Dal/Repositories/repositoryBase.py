from abc import abstractmethod
import sqlite3

from SharedResourses.logService import LogService


class RepositoryBase:

    def __init__(self, connection_string=''):
        self._setConnectionString(connection_string)
        self.logger = LogService()

    def _setConnectionString(self, connection_string):
        if(connection_string == ''):
            connection_string = 'db/pastes.db'
        self.connection_string = connection_string

    # create and return db connection instance
    def create_conection(self):
        return sqlite3.connect(self.connection_string)

    # abstract method to implement by inheritor, uses to add new Entity
    @abstractmethod
    def add(self, url):
        pass

    # abstract method to implement by inheritor, uses to get all Entity records
    @abstractmethod
    def get(self):
        pass
