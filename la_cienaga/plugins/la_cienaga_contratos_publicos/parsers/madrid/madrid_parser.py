from la_cienaga.core.abc.parser import Parser
from la_cienaga.plugins.la_cienaga_contratos_publicos.parsers.madrid.madrid_spider import MadridSpider

class MadridParser(Parser):
    title = 'madrid'
    _crawlers = [MadridSpider]

    def extract(self, data_path):
        self._extract_files(data_path)
    def transform(self, extracted):
        pass
    def load(self, transformed):
        pass

    def _extract_files(self, data_path):
        self.run_spiders()
