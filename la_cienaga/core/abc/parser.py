import abc
import os
from la_cienaga import logger
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

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
        self.load(self.transform(self.extract(data_path)))
    
    def run_spiders(self):
        """
        Inicia la ejecución de los crawlers
        """
        process = CrawlerProcess(Settings())
        for crawler in self._crawlers:
            process.crawl(crawler, config=self._config)
        process.start()

