import os
import yaml

class Config(dict):
    """
    Genera una clase que hereda de dict con facilidades para la lectura de las configuraciones. El formato siempre es YAML.
    Si se construye sin parámetros, lee la config general, si se le pasa settings_path lee el fichero de config
    pasado en el path
    """
    def __init__(self, defaults={}, settings_path=None):
        dict.__init__(self, defaults)
        if not settings_path:
            self._settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'settings.yml')
        else:
            self._settings_path = settings_path
        if os.path.isfile(self._settings_path):
            self._load(self._settings_path)

    def _load(self,settings):
        """
        Puebla el objeto con la configuración general
        """
        with open(settings, 'r') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        if config:
            for key,value in config.items():
                self[key] = value
