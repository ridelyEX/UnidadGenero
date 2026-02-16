from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Persona

class PersonaListView(LoginRequiredMixin, ListView):
    model = Persona
    template_name = 'organizacion/persona_list.html'
    context_object_name = 'personas'

class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    template_name = 'organizacion/persona_form.html'
    fields = ['nombre', 'sexo', 'cargo', 'puesto', 'departamento', 'activo']
    success_url = reverse_lazy('personas_list')

    def form_valid(self, form):
        messages.success(self.request, 'Persona registrada exitosamente.')
        return super().form_valid(form)

class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    template_name = 'organizacion/persona_form.html'
    fields = ['nombre', 'sexo', 'cargo', 'puesto', 'departamento', 'activo']
    success_url = reverse_lazy('personas_list')

    def form_valid(self, form):
        messages.success(self.request, 'Persona actualizada exitosamente.')
        return super().form_valid(form)

class PersonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Persona
    template_name = 'organizacion/persona_confirm_delete.html'
    success_url = reverse_lazy('personas_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Persona eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)
