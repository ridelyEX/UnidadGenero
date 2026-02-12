import logging
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Usuario, Rol

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        username = self.request.POST.get('username', "Desconocido")
        ip = self.request.META.get('REMOTE_ADDR', 'sin_ip')
        logger.error(f'Intento de inicio de sesión fallido para ${username}')
        messages.error(self.request, 'El usuario y la contraseña no coinciden')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')

class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = Usuario
    template_name = 'usuarios/usuario_form.html'
    fields = ['nombre', 'correo', 'password', 'id_rol', 'is_active', 'is_admin']
    success_url = reverse_lazy('usuarios_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Usuario creado exitosamente.')
        return super().form_valid(form)

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'usuarios/usuario_form.html'
    fields = ['nombre', 'correo', 'id_rol', 'is_active', 'is_admin']
    success_url = reverse_lazy('usuarios_list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuario actualizado exitosamente.')
        return super().form_valid(form)

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Usuario eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
