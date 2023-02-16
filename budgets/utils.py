from bs4 import BeautifulSoup
from django.contrib import messages
from orders.models import Supplier, Material


def xml_to_model(xml_file, model, request):
    """
    This function takes two arguments, xml_file and model
    Creates or updates a model with fields given.
    """

    # We soupify the xml_file
    soup = BeautifulSoup(xml_file, features='xml')

    # Find all the tags named 'cfdi:Concepto'
    concepts = soup.find_all('cfdi:Concepto')

    supplier = soup.find('cfdi:Emisor')
    rfc = supplier.attrs['Rfc']
    name = supplier.attrs['Nombre']
    supplier_obj, created = Supplier.objects.get_or_create(id=rfc, name=name)

    # For every tag found (which means every product added)
    # we update its values, then we saved the object
    for tag in concepts:
        try:
            obj, created = model.objects.get_or_create(id=tag['NoIdentificacion'])
            obj.name = tag['Descripcion']
            obj.quantity_ordered = float(tag['Cantidad'])
            obj.unit_code = tag['Unidad']
            obj.unit_price = float(tag['ValorUnitario'])
            obj.vat = float(tag.find('cfdi:Traslado')['TasaOCuota']) + 1
            obj.supplier_id = supplier_obj
            obj.save()
            messages.success(request, f'{tag["NoIdentificacion"]} agregado con éxito')
        except KeyError:
            messages.add_message(request, messages.WARNING, 'Uno o mas materiales NO agregados')
    return
