from la_cienaga.core.abc.parser import Parser

class MadridParser(Parser):
    title = 'madrid'

    def extract(self, data_path):
        pass
    def transform(self, extracted):
        pass
    def load(self, transformed):
        pass
