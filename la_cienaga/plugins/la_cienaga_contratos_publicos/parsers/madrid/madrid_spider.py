from scrapy.http import FormRequest, Request
from scrapy import Spider

from la_cienaga import logger

class MadridSpider(Spider):
    name = "madrid_spider"

    def start_requests(self):
        url = self.config['urls']['madrid']
        form_data = {
            '_charset_': 'UTF-8',
            'pagename': 'PortalContratacion/Comunes/Presentacion/PCON_resultadoBuscadorAvanzado',
            'language': 'es',
            'pageid': '1224915242285',
            'denominacionContrato': '',
            'tipoPublicacion': '',
            'situacion': '',
            'cpv': '',
            'compraInnovadora': '',
            'numeroExpediente': '',
            'referencia': '',
            'tipoContrato': '',
            'entidadAdjudicadora': '',
            'idOrganismoBusq': '',
            'txtOrganismo': '',
            'idSermas': '',
            'txtSermas': '',
            'idFunBio': '',
            'txtFunBio': '',
            'procedimientoAdjudicacion': '',
            'fechaPublicDesde': '',
            'fechaPublicHasta': '',
            'fechaInicDesde': '',
            'fechaInicHasta': '',
            'fechaFinDesde': '',
            'fechaFinHasta': '',
            'fechaAdjudicacionDesde': '',
            'fechaAdjudicacionHasta': '',
            'fechaFormalizacionDesde': '',
            'fechaFormalizacionHasta': '',
            'rs': '',
            'nif': '',
            'licitaDesde': '',
            'licitaHasta': '',
            'adjDesde': '',
            'adjHasta': ''
        }

        yield FormRequest(url, formdata=form_data)

    def parse(self, response):
        # Parsear todos y cada uno de los elementos presentes en la tabla
        for element in response.xpath("//div[@class='cajaBlanca']"):
            contract_url = element.xpath("./div[@class='cajaBlancaDosL']/a").attrib['href']
            yield response.follow(contract_url, callback=self.parse_contract)
        
        # seguimos a la siguiente página
        next_url = response.xpath("//div[@class='caja']/ul/li/a")[-1].attrib['href']
        pagination_symbol = response.xpath("//div[@class='caja']/ul/li/a/text()")[-1].get()

        if pagination_symbol == '>':
            yield response.follow(next_url, callback=self.parse)
    
    def parse_contract(self, response):
        pass
    
