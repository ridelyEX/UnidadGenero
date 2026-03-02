import logging
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from organizaciones.models import Persona
from .models import Usuario, Rol
from django import forms

logger = logging.getLogger(__name__)

class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = Usuario
    template_name = 'usuarios/usuario_form.html'
    fields = ['nombre', 'correo', 'password', 'persona','id_rol', 'is_active', 'is_admin']
    success_url = reverse_lazy('usuarios_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['id_rol'].label_from_instance = lambda obj: f"{obj.descripcion}"

        form.fields['persona'].queryset = Persona.objects.filter(usuario__isnull=True)
        form.fields['persona'].label_from_instance = lambda obj: f"{obj.nombre}"
        form.fields['persona'].required = True

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Rol.objects.all()
        context['personas'] = Persona.objects.all()
        return context

    def form_valid(self, form):
        persona_seleccionada = form.cleaned_data.get('persona')

        try:
            if persona_seleccionada.usuario:
                messages.error(self.request, 'Esta perosona ya tiene un usuario asociado')
                return self.form_invalid(form)
        except Usuario.DoesNotExist:
            pass

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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['id_rol'].label_from_instance = lambda obj: f"{obj.descripcion}"
        return form

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
