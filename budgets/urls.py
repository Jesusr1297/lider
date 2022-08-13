from django.urls import path
from .views import (budget, MaterialsView, MaterialsCreateView,
                    MaterialsDetailView, MaterialsDeleteView,
                    MaterialUpdateView)

urlpatterns = [
    path('', budget, name='budgets'),
    path('materiales/', MaterialsView.as_view(), name='materials'),
    path('materiales/agregar/', MaterialsCreateView.as_view(), name='material-create'),
    path('materiales/detalle/<int:pk>', MaterialsDetailView.as_view(), name='material-detail'),
    path('materiales/eliminar/<int:pk>', MaterialsDeleteView.as_view(), name='material-delete'),
    path('materiales/editar/<int:pk>', MaterialUpdateView.as_view(), name='material-update')
]
