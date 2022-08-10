from django.urls import path
from .views import budget, MaterialsView

urlpatterns = [
    path('', budget, name='budgets'),
    path('materiales/', MaterialsView.as_view(), name='materials')
]
