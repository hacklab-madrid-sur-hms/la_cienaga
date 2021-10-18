from scrapy.http import Request, HtmlResponse
from la_cienaga.plugins.la_cienaga_contratos_publicos.parsers.madrid.madrid_spider import MadridSpider
import pytest
import os.path

@pytest.fixture
def load_4118600_response():
    url = 'http://www.madrid.org/cs/Satellite?c=CM_ConvocaPrestac_FA&cid=1354881221028&definicion=Contratos+Publicos&idPagina=1224915242285&language=es&op2=PCON&pagename=PortalContratacion%2FPage%2FPCON_contratosPublicos&tipoServicio=CM_ConvocaPrestac_FA'
    filedir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(filedir, 'resources', '4118600.html'), 'rb') as f:
        html_content = f.read()
    
    request = Request(url)
    response = HtmlResponse(url=url, request=request, body=html_content)

    return response

@pytest.fixture
def load_2788420_response():
    url = 'https://www.madrid.org/cs/Satellite?c=CM_ConvocaPrestac_FA&cid=1354758585304&definicion=Contratos+Publicos&idPagina=1224915242285&language=es&op2=PCON&pagename=PortalContratacion%2FPage%2FPCON_contratosPublicos&tipoServicio=CM_ConvocaPrestac_FA'
    filedir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(filedir, 'resources', '2788420.html'), 'rb') as f:
        html_content = f.read()
    
    request = Request(url)
    response = HtmlResponse(url=url, request=request, body=html_content)

    return response

@pytest.fixture
def load_madrid_spider():
    spider = MadridSpider()

    return spider

def test_2788420(load_2788420_response, load_madrid_spider):
    item = load_madrid_spider.parse_contract(load_2788420_response)
    assert True

def test_4118600(load_4118600_response, load_madrid_spider):
    item = load_madrid_spider.parse_contract(load_4118600_response)
    assert len(item) == 23 # Son 23 campos a obtener en este contrato
    ## Detalle del contrato ##
    ## Principales
    assert item['titulo'] == 'Suministro de cementos óseos y accesorios para cementación, biomateriales y diverso fungible para el servicio de traumatología del Hospital Universitario de Fuenlabrada'
    assert item['fecha_convocatoria'] == 'Convocatoria publicada el 26 mayo 2021 12:30'
    assert item['estado'] == 'En tramitación'
    assert item['fecha_fin_presentacion'] == 'Fin:29 junio 2021'
    assert item['estado_de_la_licitacion'] == 'Adjudicada'
    assert item['tipo_publicacion'] == 'Convocatoria anunciada a licitación'
    assert item['objeto_del_contrato'] == 'Suministro de cementos óseos y accesorios para cementación, biomateriales y diverso fungible para el servicio de traumatología del Hospital Universitario de Fuenlabrada'
    assert item['codigo_cpv'] == '33184100-4'
    assert item['compra_publica_innovadora'] == False
    assert item['numero_de_expediente'] == 'PA SUM 21-024'
    assert item['referencia'] == '4118600'
    assert item['tipo_de_contrato'] == 'Suministros'
    assert item['entidad_adjudicadora'] == 'Consejería de Sanidad - Hospital Universitario de Fuenlabrada'
    assert item['codigo_nuts'] == 'ES300'
    assert item['procedimiento_adjudicacion'] == 'Abierto'
    assert item['valor_estimado_sin_i_v_a'] == 408545.51
    assert item['presupuesto_base_licitacion_sin_impuestos'] == 151313.15
    assert item['presupuesto_base_licitacion_importe_total'] == 172263.47
    assert item['duracion_del_contrato'] == '24 Meses'
    assert item['fecha_limite_de_presentacion_de_ofertas_o_solicitudes_de_participacion'] == '29 junio 2021 14:00'
    assert item['puntos_de_informacion'] == '* Obtención de documentación e información: - - Hospital Universitario de Fuenlabrada - Área de Suministros, de lunes a viernes, de 09:00 a 14:00 horas. Camino del molino, 2. Fuenlabrada-Madrid 28942. Teléfono: 91 6009624/ 91 6006732. Fax: 91 6006712. - - Correo electrónico: suministros.hflr@salud.madrid.org . - - Dirección de Internet: http://www.hospitaldefuenlabrada.org - - Oficinas de Atención al Ciudadano. - * Presentación de ofertas o de solicitudes de participación: - Presentación electrónica accediendo a la plataforma electrónica de contratación pública del Hospital Universitario de Fuenlabrada en la URL: community.vortal.biz/PRODSTS/Users/Login/Index, donde está disponible la información necesaria. - *Apertura de ofertas: - Hospital Universitario de Fuenlabrada. Camino del molino, 2. 28942 Fuenlabrada-Madrid.'
    assert item['adjudicacion_del_contrato_publicada_el'] == '22 septiembre 2021'
    ## Adjudicatarios por lotes
    assert item['resultado_adjudicacion']['importe_total_adjudicacion'] == 122606
    adj_info = [{'importe_adjudicacion_con_iva': 12650.0,
 'importe_adjudicacion_sin_iva': 11500.0,
 'nif_adjudicatario': 'B15205537',
 'nolote': None,
 'nombre_o_razon_social_adjudicatario': 'CMM, S.L.U',
 'noofertas': 13,
 'resultado': 'Adjudicado'}, {'importe_adjudicacion_con_iva': 17963.0,        
 'importe_adjudicacion_sin_iva': 16330.0,
 'nif_adjudicatario': 'B62162326',
 'nolote': None,
 'nombre_o_razon_social_adjudicatario': 'A2C SUMINISTROS HOSPITALARIOS, S.L.',
 'noofertas': 13,
 'resultado': 'Adjudicado'}, {'importe_adjudicacion_con_iva': 15840.0,        
 'importe_adjudicacion_sin_iva': 14400.0,
 'nif_adjudicatario': 'A28123297',
 'nolote': None,
 'nombre_o_razon_social_adjudicatario': 'SMITH NEPHEW S A.',
 'noofertas': 13,
 'resultado': 'Adjudicado'}, {'importe_adjudicacion_con_iva': 11357.5,        
 'importe_adjudicacion_sin_iva': 10325.0,
 'nif_adjudicatario': 'A81726655',
 'nolote': None,
 'nombre_o_razon_social_adjudicatario': 'ORTO MEDIMATEC S A.U',
 'noofertas': 13,
 'resultado': 'Adjudicado'}, {'importe_adjudicacion_con_iva': 17325.0,
 'importe_adjudicacion_sin_iva': 15750.0,
 'nif_adjudicatario': 'B84463165',
 'nolote': None,
 'nombre_o_razon_social_adjudicatario': 'MAXILARIA SURGERY S.L.',
 'noofertas': 13,
 'resultado': 'Adjudicado'}, {'importe_adjudicacion_con_iva': 16087.5,
 'importe_adjudicacion_sin_iva': 14625.0,
 'nif_adjudicatario': 'ARTHREX ESPAÑA, S.L.',
 'nolote': None,
 'nombre_o_razon_social_adjudicatario': 'ARTHREX ESPAÑA, S.L.',
 'noofertas': 13,
 'resultado': 'Adjudicado'}, {'importe_adjudicacion_con_iva': 10758.0,
 'importe_adjudicacion_sin_iva': 9780.0,
 'nif_adjudicatario': 'B46012696',
 'nolote': None,
 'nombre_o_razon_social_adjudicatario': 'BAXTER S L.',
 'noofertas': 13,
 'resultado': 'Adjudicado'}, {'importe_adjudicacion_con_iva': 20625.0,
 'importe_adjudicacion_sin_iva': 18750.0,
 'nif_adjudicatario': 'B29060381',
 'nolote': None,
 'nombre_o_razon_social_adjudicatario': 'ZIMMER BIOMET SPAIN, S.L.U.',
 'noofertas': 13,
 'resultado': 'Adjudicado'}]
    assert item['resultado_adjudicacion']['adjudicatarios'] == adj_info
    ## ##