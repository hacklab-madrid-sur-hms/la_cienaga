import pkgutil
import inspect
import os
from la_cienaga import logger
from la_cienaga.core.abc.plugin import Plugin
from importlib import import_module
from la_cienaga.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Parser plugins'
    def add_arguments(self, parser):
        parser.add_argument('--plugin-list', '-l', nargs='+', default=[], help='Parse specified plugins')

    def handle(self, *args, **options):
        if options['plugin_list']:
            self._parse_plugin_list(options['plugin_list'])
        else:
            self._parse_all()

    def _parse_plugin_list(self, plugins):
        print('PARSE LIST')

    def _parse_all(self):
        plugins_list = [name for _, name, is_pkg in pkgutil.iter_modules([self.plugins_dir])
            if is_pkg and not name.startswith('_')]

        for plugin in plugins_list:
            logger.info(f'Parseando Plugin: {plugin}')
            plugin_obj = self._load_plugin_class(plugin)
            plugin_path = os.path.dirname(inspect.getfile(plugin_obj.__class__))
            if os.path.isfile(os.path.join(plugin_path, 'config.yml')):
                plugin_obj.load_config(os.path.join(plugin_path, 'config.yml'))
            if os.path.isdir(os.path.join(plugin_path, 'config')) and os.path.isfile(os.path.join(plugin_path, 'config', 'config.yml')):
                plugin_obj.load_config(os.path.join(plugin_path, 'config', 'config.yml'))
            plugin_obj.parse()


    def _load_plugin_class(self, name):
        subclasses = []
        module = import_module('la_cienaga.plugins.%s' % name)
        subclasses = [obj for name, obj in inspect.getmembers(module) if inspect.isclass(obj) and issubclass(obj, Plugin) and name != 'Plugin']
        if len(subclasses) == 1:
            return subclasses[0]()
