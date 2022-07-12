from django.shortcuts import render
from .models import (Order, Lider, Customer)


# Create your views here.
def test_view(request):
    context = {
        'orders': Order.objects.all()
    }
    return render(request, template_name='crm/order.html', context=context)
