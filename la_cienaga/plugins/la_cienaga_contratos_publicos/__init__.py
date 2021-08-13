from la_cienaga.core.plugin import Plugin

class ContratosPublicosPlugin(Plugin):
    def parse():
        """
        Método que implementa el parseo del plugin.
        En este caso, es un plugin compuesto por lo que llamará a cada uno
        de los parsers de cada uno de los subplugins (madrid, cantabria, galicia, ...).
        """
        pass