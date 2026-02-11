from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Indicador

class IndicadorListView(LoginRequiredMixin, ListView):
    model = Indicador
    template_name = 'indicadores/indicador_list.html'
    context_object_name = 'indicadores'

class IndicadorCreateView(LoginRequiredMixin, CreateView):
    model = Indicador
    template_name = 'indicadores/indicador_form.html'
    fields = ['nombre', 'descripcion', 'tipo', 'periodicidad', 'fecha']
    success_url = reverse_lazy('indicadores_list')

    def form_valid(self, form):
        messages.success(self.request, 'Indicador registrado correctamente.')
        return super().form_valid(form)

class IndicadorUpdateView(LoginRequiredMixin, UpdateView):
    model = Indicador
    template_name = 'indicadores/indicador_form.html'
    fields = ['nombre', 'descripcion', 'tipo', 'periodicidad', 'fecha']
    success_url = reverse_lazy('indicadores_list')

    def form_valid(self, form):
        messages.success(self.request, 'Indicador actualizado correctamente.')
        return super().form_valid(form)

class IndicadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Indicador
    template_name = 'indicadores/indicador_confirm_delete.html'
    success_url = reverse_lazy('indicadores_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Indicador eliminado correctamente.')
        return super().delete(request, *args, **kwargs)
