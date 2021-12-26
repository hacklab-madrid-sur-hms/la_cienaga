from la_cienaga import settings
import os
import yaml
import abc

class DB(metaclass=abc.ABCMeta):
    def __init__(self):
        self._mongo_connection = settings['mongo_connection']

    @abc.abstractmethod
    def connect(self, db):
        pass
