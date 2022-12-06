from django.urls import path
from .views import (LiderView, LiderCreateView, LiderDetailView,
                    LiderUpdateView, LiderDeleteView)

urlpatterns = [
    path('', LiderView.as_view(), name='lider'),
    path('crear/', LiderCreateView.as_view(), name='lider-create'),
    path('detalle/<int:pk>/', LiderDetailView.as_view(), name='lider-detail'),
    path('editar/<int:pk>/', LiderUpdateView.as_view(), name='lider-update'),
    path('eliminar/<int:pk>/', LiderDeleteView.as_view(), name='lider-delete'),
]
