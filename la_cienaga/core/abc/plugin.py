from la_cienaga import settings
from la_cienaga.core.config import Config
import os
import yaml
import pkgutil
import importlib
import inspect
import sys

class Plugin(object):
    """
    La clase Plugin implementa la funcionalidad básica del parseado y de la
    robotización.
    """

    def __init__(self):
        self._parsers = []
        self._config = None
        self._parser_path = None
        self._data_path = None
        self._plugin_name = None

    @property
    def parsers(self):
        return self._parsers

    @parsers.setter
    def parsers(self, value):
        self._parsers = value

    @property
    def config(self):
        return self._config

    @property
    def parser_path(self):
        return self._parser_path

    @parser_path.setter
    def parser_path(self, value):
        self._parser_path = value

    @property
    def data_path(self):
        return self._data_path

    @data_path.setter
    def data_path(self, value):
        self._data_path = value

    @property
    def plugin_name(self):
        return self._plugin_name

    @plugin_name.setter
    def plugin_name(self, value):
        self._plugin_name = value

    def load_config(self,config_path):
        """
        Carga la configuración a partir de los path de config generales y particulares de cada plugin.
        """
        gen_settings = dict(settings)
        self._config_path = config_path
        config = Config(settings_path=config_path)

        gen_settings.update(config)

        self._config = gen_settings

    def check_config(self):
        """
        Comprueba que las claves obligatorias existen en el fichero de configuración del plugin
        """
        error_msg = 'La clave obligatoria %s no está en el fichero de configuración %s'
        if not 'title' in self._config:
            raise ValueError(error_msg % ('title', self._config_path))
        if not 'parser_dir' in self._config:
            raise ValueError(error_msg % ('parser_dir', self._config_path))
        if not 'data_dir' in self._config:
            raise ValueError(error_msg % ('data_dir', self._config_path))
        if not 'urls' in self._config:
            raise ValueError(error_msg % ('urls', self._config_path))
        if not 'mongo_connection' in self._config:
            raise ValueError(error_msg % ('mongo_connection', self._config_path))

    def load_parsers(self):
        """
        Genera la lista de parsers de los plugins y la puebla con instancias de los mismos.
        Considerará un parser todo aquel fichero fuente que contenga la subcadena 'parser' en el nombre del fichero.
        """
        parsers = []
        modulepath = 'la_cienaga.plugins.%s.%s' % (self._plugin_name, self._config['parser_dir'])
        packages = [name for _,name,is_pkg in pkgutil.walk_packages([self._parser_path]) if is_pkg]
        for package in packages:
            modules = [name for _,name,is_pkg in pkgutil.iter_modules([os.path.join(self.parser_path, package)]) if not is_pkg]
            for module in modules:
                if 'parser' in module:
                    classpath = '.'.join([modulepath, package, module])
                    imported_module = importlib.import_module(classpath)
                    classname = [name for name, obj in inspect.getmembers(imported_module, inspect.isclass)][0]
                    klass = getattr(imported_module, classname)
                    instance = klass()
                    instance.config = self._config
                    parsers.append(instance)
        self._parsers = parsers

    def parse(self):
        """
        A partir de la lista de parsers, ejecuta el parseado llamando al método parse() de cada parser.
        """
        if self.parsers:
            for parser in self.parsers:
                parser.parse(self._data_path)
        else:
            raise ValueError('No se ha instanciado el atributo parsers')
