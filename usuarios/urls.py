from django.urls import path, include
from django.contrib.auth.views import LogoutView

from unidad_genero.urls import handler404
from .views import (
    CustomLoginView, UsuarioListView, UsuarioCreateView,
    UsuarioUpdateView, UsuarioDeleteView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('usuarios/', UsuarioListView.as_view(), name='usuarios_list'),
    path('usuarios/nuevo/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='usuario_delete'),
]
