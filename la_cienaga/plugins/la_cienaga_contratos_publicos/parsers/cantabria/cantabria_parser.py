import os
import time
import calendar
import requests
import datetime
import json

from la_cienaga.core.abc.parser import Parser
from la_cienaga import logger
from string import Template

class CantabriaParser(Parser):
    title = 'cantabria'

    def extract(self, data_path):
        pass
    def transform(self, extracted):
        pass
    def load(self, transformed):
        pass