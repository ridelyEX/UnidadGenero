from django import forms
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Caso_atencion

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

class CasoListView(AdminRequiredMixin, ListView):
    model = Caso_atencion
    template_name = 'casos/caso_list.html'
    context_object_name = 'casos'

class CasoCreateView(AdminRequiredMixin, CreateView):
    model = Caso_atencion
    template_name = 'casos/caso_form.html'
    fields = ['tipo', 'jerarquia_acoso', 'fecha', 'estatus', 'medidas']
    success_url = reverse_lazy('casos_list')

    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        form.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Caso registrado exitosamente.')
        return super().form_valid(form)

class CasoUpdateView(AdminRequiredMixin, UpdateView):
    model = Caso_atencion
    template_name = 'casos/caso_form.html'
    fields = ['tipo', 'fecha', 'estatus', 'medidas']
    success_url = reverse_lazy('casos_list')

    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        form.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Caso actualizado exitosamente.')
        return super().form_valid(form)

class CasoDeleteView(AdminRequiredMixin, DeleteView):
    model = Caso_atencion
    template_name = 'casos/caso_confirm_delete.html'
    success_url = reverse_lazy('casos_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Caso eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
