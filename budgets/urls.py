from django.urls import path
from .views import budget

urlpatterns = [
    path('cotizaciones/', budget, name='budgets')
]
