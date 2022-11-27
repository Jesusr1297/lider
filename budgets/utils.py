from bs4 import BeautifulSoup
import json


def xml_to_model(xml, model):
    soup = BeautifulSoup(xml, features='xml')
    concepts = soup.find_all('cfdi:Concepto')
    for tag in concepts:
        obj, created = model.objects.get_or_create(id=tag['NoIdentificacion'])
        obj.name = tag['Descripcion']
        obj.quantity_ordered = float(tag['Cantidad'])
        obj.unit_code = tag['Unidad']
        obj.unit_price = float(tag['ValorUnitario'])
        obj.vat = float(tag.find('cfdi:Traslado')['TasaOCuota']) + 1
        obj.save()
    return
