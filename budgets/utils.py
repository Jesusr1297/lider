from bs4 import BeautifulSoup
import glob
import json


def xml_products(path=None):
    if path is None:
        return json.dumps({})

    print(path + '/*.xml')
    xml_list = glob.glob(path + '/*.xml')
    print(xml_list)
    products = []

    for xml in xml_list:
        with open(xml) as f:
            data = f.read()

        soup = BeautifulSoup(data, xml)
        concepts = soup.find_all('cfdi:Concepto')

        for tag in concepts:
            products.append({
                'id': tag['NoIdentificacion'],
                'name': tag['Descripcion'],
                'quantity_ordered': tag['Cantidad'],
                'unit_code': tag['Unidad'],
                'unit_price': tag['ValorUnitario'],
                'vat': tag.find('cfdi:Traslado')['TasaOCuota']
            })

    return json.dumps(products)
