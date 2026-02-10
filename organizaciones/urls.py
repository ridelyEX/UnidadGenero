from django.urls import path
from .views import (
    PersonaListView, PersonaCreateView,
    PersonaUpdateView, PersonaDeleteView
)

urlpatterns = [
    path('personas/', PersonaListView.as_view(), name='personas_list'),
    path('personas/nueva/', PersonaCreateView.as_view(), name='persona_create'),
    path('personas/<int:pk>/editar/', PersonaUpdateView.as_view(), name='persona_update'),
    path('personas/<int:pk>/eliminar/', PersonaDeleteView.as_view(), name='persona_delete'),
]
