from django.urls import path
from .views import (
    IndicadorListView, IndicadorCreateView,
    IndicadorUpdateView, IndicadorDeleteView
)

urlpatterns = [
    path('indicadores/', IndicadorListView.as_view(), name='indicadores_list'),
    path('indicadores/nuevo/', IndicadorCreateView.as_view(), name='indicador_create'),
    path('indicadores/<int:pk>/editar/', IndicadorUpdateView.as_view(), name='indicador_update'),
    path('indicadores/<int:pk>/eliminar/', IndicadorDeleteView.as_view(), name='indicador_delete'),
]
