import os
import yaml

class Plugin(object):
    """
    La clase Plugin implementa la funcionalidad básica del parseado y de la
    robotización.
    """

    def __init__(self):
        self._parsers = []
        self._config = None

    @property
    def parsers(self):
        return self._parsers

    @parsers.setter
    def parsers(self, value):
        self._parsers = value

    @property
    def config(self):
        return self._config

    def load_config(self,path):
        with open(path, 'r') as f:
            self._config = yaml.load(f, Loader=yaml.SafeLoader)

    def parse(self):
        if self.parsers:
            for parser in self.parsers:
                parser.parse()
        else:
            raise ValueError('No se ha instanciado el atributo parsers')
