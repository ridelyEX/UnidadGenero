from django.urls import path
from .views import (
    CasoListView, CasoCreateView,
    CasoUpdateView, CasoDeleteView, CasoCloseView
)

urlpatterns = [
    path('expediente/', CasoListView.as_view(), name='expediente_list'),
    path('expediente/nuevo/', CasoCreateView.as_view(), name='expediente_create'),
    path('expediente/<int:pk>/editar/', CasoUpdateView.as_view(), name='expediente_update'),
    path('expediente/<int:pk>/cerrar/', CasoCloseView.as_view(), name='expediente_cerrar'),
    path('expediente/<int:pk>/eliminar/', CasoDeleteView.as_view(), name='expediente_delete'),
]
