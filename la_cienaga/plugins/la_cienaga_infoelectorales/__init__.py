from la_cienaga import logger
from la_cienaga.core.plugin import Plugin

class InfoelectoralesPlugin(Plugin):
    def parse(self):
        """
        Método que implementa el parseo del plugin.
        En este caso, es un plugin compuesto por lo que llamará a cada uno
        de los parsers de cada uno de los subplugins (madrid, cantabria, galicia, ...).
        """
        pass
