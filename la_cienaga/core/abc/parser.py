import abc
from la_cienaga import logger

class Parser(metaclass=abc.ABCMeta):
    title = ''

    @abc.abstractmethod
    def extract(self):
        pass
    @abc.abstractmethod
    def transform(self, extracted):
        pass
    @abc.abstractmethod
    def load(self, transformed):
        pass

    def parse(self):
        logger.info('Ejecutando parser: %s' % self.title)
        self.load(self.transform(self.extract()))
