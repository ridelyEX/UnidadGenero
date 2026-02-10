from django.urls import path
from .views import (
    ActividadListView, ActividadCreateView, ActividadUpdateView, ActividadDeleteView,
    DocumentoListView, DocumentoCreateView, DocumentoDeleteView,
    BitacoraListView,
    CapacitacionListView, CapacitacionCreateView, CapacitacionUpdateView, CapacitacionDeleteView
)

urlpatterns = [
    # Actividades
    path('actividades/', ActividadListView.as_view(), name='actividades_list'),
    path('actividades/nueva/', ActividadCreateView.as_view(), name='actividad_create'),
    path('actividades/<int:pk>/editar/', ActividadUpdateView.as_view(), name='actividad_update'),
    path('actividades/<int:pk>/eliminar/', ActividadDeleteView.as_view(), name='actividad_delete'),

    # Documentos
    path('documentos/', DocumentoListView.as_view(), name='documentos_list'),
    path('documentos/nuevo/', DocumentoCreateView.as_view(), name='documento_create'),
    path('documentos/<int:pk>/eliminar/', DocumentoDeleteView.as_view(), name='documento_delete'),

    # Bitacora
    path('bitacora/', BitacoraListView.as_view(), name='bitacora_list'),

    # Capacitaciones
    path('capacitaciones/', CapacitacionListView.as_view(), name='capacitaciones_list'),
    path('capacitaciones/nueva/', CapacitacionCreateView.as_view(), name='capacitacion_create'),
    path('capacitaciones/<int:pk>/editar/', CapacitacionUpdateView.as_view(), name='capacitacion_update'),
    path('capacitaciones/<int:pk>/eliminar/', CapacitacionDeleteView.as_view(), name='capacitacion_delete'),
]
