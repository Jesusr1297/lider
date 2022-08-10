from django.urls import path
from .views import budget, MaterialsView, MaterialsCreateView

urlpatterns = [
    path('', budget, name='budgets'),
    path('materiales/', MaterialsView.as_view(), name='materials'),
    path('materiales/agregar', MaterialsCreateView.as_view(), name='material-create'),
]
