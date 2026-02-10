from django.urls import path
from .views import (
    CasoListView, CasoCreateView,
    CasoUpdateView, CasoDeleteView
)

urlpatterns = [
    path('casos/', CasoListView.as_view(), name='casos_list'),
    path('casos/nuevo/', CasoCreateView.as_view(), name='caso_create'),
    path('casos/<int:pk>/editar/', CasoUpdateView.as_view(), name='caso_update'),
    path('casos/<int:pk>/eliminar/', CasoDeleteView.as_view(), name='caso_delete'),
]
