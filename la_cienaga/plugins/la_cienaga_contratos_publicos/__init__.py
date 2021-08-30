from la_cienaga import logger
from la_cienaga.core.abc.plugin import Plugin
from la_cienaga.plugins.la_cienaga_contratos_publicos.parsers.madrid.parser import MadridParser
from la_cienaga.plugins.la_cienaga_contratos_publicos.parsers.cantabria.parser import CantabriaParser

class ContratosPublicosPlugin(Plugin):
    def __init__(self):
        madrid_parser = MadridParser()
        cantabria_parser = CantabriaParser()
        self.parsers = [madrid_parser, cantabria_parser]
