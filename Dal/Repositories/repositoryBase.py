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

    def create_conection(self):
        return sqlite3.connect(self.connection_string)

    @abstractmethod
    def add(self, url):
        pass

    @abstractmethod
    def get(self):
        pass
