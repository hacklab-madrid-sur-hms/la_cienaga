import os
import time
import calendar
import requests
import datetime

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dateutil.rrule import rrule, DAILY
from la_cienaga.core.abc.parser import Parser
from la_cienaga import logger
from string import Template

class CantabriaParser(Parser):
    title = 'cantabria'

    def extract(self, data_path):
        self._extract_files(data_path)
    def transform(self, extracted):
        pass
    def load(self, transformed):
        pass

    def _extract_files(self, data_path):
        """
        A partir de la url de descarga que autogenera el csv, descargamos un csv de contratos públicos
        desde el 01/01/2015 por día para, después, juntarlo y generar los objetos que se pasaran al proceso de
        transformación
        """
        # Eliminamos el contenido del directorio de descargas
        self.remove_dir_content(data_path)
        # Configuramos el Incremental Retry de la conexión
        session = requests.Session()
        retries = Retry(total=10, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], method_whitelist=['HEAD', 'GET', 'OPTIONS'])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        # Cargamos la plantilla de url
        template = Template(self._config['urls'][self.title]['contratos_publicos'])
        current_date = datetime.datetime.now()
        start_date = datetime.datetime(2015,1,1)
        # Iteramos sobre todos los días desde el 15-01-01 al día actual y descargamos sus contratos

        for c_date in rrule(freq=DAILY, dtstart=start_date, until=current_date):
            c_date_str = c_date.strftime('%Y-%m-%d')
            url = template.substitute(fecha_inicio=c_date_str, fecha_fin=c_date_str)
            logger.info('Descargando datos del día %s' % c_date_str)
            if not self.is_downloaded(c_date):
                self._download(url, data_path, session=session)
                time.sleep(10)

    def is_downloaded(self,date):
        return  False

    def _download(self, url, data_path, session=None):
        if session:
            r = session.get(url)
        else:
            r = requests.get(url)
        content_disposition = r.headers.get('content-disposition')
        if content_disposition:
            filename = content_disposition.split(';')[1][9:]
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            with open(os.path.join(data_path, filename), 'wb') as f:
                f.write(r.content)
        else:
            logger.warn('No ha sido posible encontrar contratos')
