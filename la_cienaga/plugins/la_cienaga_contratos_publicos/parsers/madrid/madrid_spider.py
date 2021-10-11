import locale
import unicodedata
from babel.numbers import parse_decimal
from slugify import slugify
from datetime import datetime as dt
from scrapy.http import FormRequest, Request
from scrapy import Spider
from la_cienaga.plugins.la_cienaga_contratos_publicos.parsers.madrid.madrid_items import MadridItem, AdjudicacionMadridItem

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
        locale.setlocale(locale.LC_TIME, 'es_ES')
        madrid_fields = {}
        titulo = unicodedata.normalize('NFKD', response.xpath("//div[@id='titulo_cabecera']/h2[@class='tit11gr3']/text()").get().strip())
        madrid_fields['titulo'] = titulo
        fecha_convocatoria_raw = response.xpath("//div[@id='titulo_cabecera']/div[@class='txt08gr3c']/text()").get()
        if fecha_convocatoria_raw:
            fecha_convocatoria_raw = unicodedata.normalize('NFKD', fecha_convocatoria_raw.strip())
            fecha_convocatoria = dt.strptime(fecha_convocatoria_raw, 'Convocatoria publicada el %d %B %Y %H:%M').strftime('%Y-%m-%d %H:%M')
            madrid_fields['fecha_convocatoria'] = fecha_convocatoria
        estado_raw = response.xpath("//div[@id='cont_int_izdo']/span[@class='txt07nar']/text()").get()
        if estado_raw:
            estado = unicodedata.normalize('NFKD', estado_raw.strip())
            madrid_fields['estado'] = estado
        fecha_fin_presentacion_raw = response.xpath("//div[@id='cont_int_izdo']/span[@class='txt07gr3']/text()").get()
        if fecha_fin_presentacion_raw:
            fecha_fin_presentacion_raw = unicodedata.normalize('NFKD', fecha_fin_presentacion_raw.strip())
            fecha_fin_presentacion = dt.strptime(fecha_fin_presentacion_raw, 'Fin:%d %B %Y').strftime('%Y-%m-%d')
            madrid_fields['fecha_fin_presentacion'] = fecha_fin_presentacion
        
        fields = {}
        for list_element in response.xpath("//div[@class='listado']"):
            for element in list_element.xpath("./ul/li[@class='txt08gr3']"):
                # Se comprueba si la etiqueta <li> contiene una tabla
                table_tag = element.xpath("./table[@class='tableAdjudicacion']")
                s_tabla = len(table_tag)
                if s_tabla > 0:
                    # si la contiene, es la tabla de adjudicación y hay que
                    # tratarla de forma distinta
                    adj_fields = []
                    columns = [slugify(header.get(), separator='_') for header in table_tag.xpath("./thead/tr/th[@id='tAdjudicaciones' and @colspan='1']/span/text()")]
                    suma_adj = 0.0
                    for row in table_tag.xpath("./tbody/tr"):
                        row_dict = {}
                        for idx, value in enumerate(row.xpath("./td")):
                            val = value.xpath('./text()')
                            adj_title = columns[idx]
                            adj_value = unicodedata.normalize('NFKD', val.get().strip()) if val.get() else val.get()
                            if adj_title == 'importe_adjudicacion_con_iva' or adj_title == 'importe_adjudicacion_sin_iva':
                                adj_value = float(parse_decimal(adj_value, locale='es'))
                                if adj_title == 'importe_adjudicacion_con_iva':
                                    suma_adj = suma_adj + adj_value
                            if adj_title == 'noofertas':
                                adj_value = int(adj_value)
                            row_dict[adj_title] = adj_value
                        # Generamos los datos de adjudicación a partir del diccionario
                        row_adj = AdjudicacionMadridItem(row_dict)
                        adj_fields.append(row_adj)
                    fields['resultado_adjudicacion'] = {
                        'adjudicatarios': adj_fields,
                        'importe_total_adjudicacion': suma_adj
                    }
                else:
                    # Si no, son el resto de campos. Se tratan de la forma estándar.
                    field_name = element.xpath("./strong/text()").get()
                    field_values = element.xpath('./text()').getall()
                    if field_name:
                        field_title = slugify(field_name, separator='_')
                        values = ' - '.join(list(filter(lambda item: item,[unicodedata.normalize('NFKD',el.strip()) for el in field_values])))
                        if field_title == 'compra_publica_innovadora':
                            values = False if values == 'No' else True
                        if field_title == 'fecha_limite_de_presentacion_de_ofertas_o_solicitudes_de_participacion':
                            values = dt.strptime(values, '%d %B %Y  %H:%M').strftime('%Y-%m-%d %H:%M')
                        if field_title == 'valor_estimado_sin_i_v_a' or field_title == 'presupuesto_base_licitacion_sin_impuestos' or field_title == 'presupuesto_base_licitacion_importe_total':
                            values = float(parse_decimal(values.split()[0], locale='es'))
                        if field_title == 'adjudicacion_del_contrato_publicada_el':
                            values = dt.strptime(values, '%d %B %Y').strftime('%Y-%m-%d')
                        fields[field_title] = values
        # Generamos el item a partir del diccionario
        madrid_fields.update(fields)
        madrid_item = MadridItem (madrid_fields)

        return madrid_item