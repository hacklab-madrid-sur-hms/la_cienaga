import abc
import os
from la_cienaga import logger
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

class Parser(metaclass=abc.ABCMeta):
    title = ''

    @abc.abstractmethod
    def extract(self, data_path):
        pass
    @abc.abstractmethod
    def transform(self):
        pass
    @abc.abstractmethod
    def load(self):
        pass

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def remove_dir_content(self, path):
        if os.path.exists(path):
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                if os.path.isfile(filepath) or os.path.islink(filepath):
                    os.unlink(filepath)

    def parse(self, data_path):
        logger.info('Ejecutando parser: %s' % self.title)
        # extrae los datos y los persiste en un repo en bruto
        self.extract(data_path)
        # obtiene los datos del repo en bruto y hace las transformaciones adecuadas
        self.transform()
        # obtiene los datos transformados del repo en bruto y los persiste en el repo
        self.load() # los c
    
    def run_spiders(self):
        """
        Inicia la ejecución de los crawlers
        """
        settings = Settings()
        process = CrawlerProcess(settings)
        logger.getLogger('scrapy').setLevel(logger.INFO)
        for crawler in self._crawlers:
            process.crawl(crawler, config=self._config)
        process.start()

