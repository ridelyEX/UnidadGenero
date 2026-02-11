from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Actividad, Documento, Bitacora

# --- Actividad Views ---
class ActividadListView(LoginRequiredMixin, ListView):
    model = Actividad
    template_name = 'gestion/actividad_list.html'
    context_object_name = 'actividades'

class ActividadCreateView(LoginRequiredMixin, CreateView):
    model = Actividad
    template_name = 'gestion/actividad_form.html'
    fields = ['tipo_actividad', 'objetivo', 'fecha_inicio', 'estatus', 'id_usuario_responsable']
    success_url = reverse_lazy('actividades_list')

    def form_valid(self, form):
        messages.success(self.request, 'Actividad creada correctamente.')
        return super().form_valid(form)

class ActividadUpdateView(LoginRequiredMixin, UpdateView):
    model = Actividad
    template_name = 'gestion/actividad_form.html'
    fields = ['tipo_actividad', 'objetivo', 'fecha_inicio', 'estatus', 'id_usuario_responsable']
    success_url = reverse_lazy('actividades_list')

    def form_valid(self, form):
        messages.success(self.request, 'Actividad actualizada correctamente.')
        return super().form_valid(form)

class ActividadDeleteView(LoginRequiredMixin, DeleteView):
    model = Actividad
    template_name = 'gestion/actividad_confirm_delete.html'
    success_url = reverse_lazy('actividades_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Actividad eliminada correctamente.')
        return super().delete(request, *args, **kwargs)

# --- Documento Views ---
class DocumentoListView(LoginRequiredMixin, ListView):
    model = Documento
    template_name = 'gestion/documento_list.html'
    context_object_name = 'documentos'

class DocumentoCreateView(LoginRequiredMixin, CreateView):
    model = Documento
    template_name = 'gestion/documento_form.html'
    fields = ['nombre_archivo', 'tipo_documento', 'ruta_archivo', 'version', 'estado', 'id_actividad']
    success_url = reverse_lazy('documentos_list')

    def form_valid(self, form):
        form.instance.id_usuario = self.request.user
        messages.success(self.request, 'Documento subido correctamente.')
        return super().form_valid(form)

class DocumentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Documento
    template_name = 'gestion/documento_confirm_delete.html'
    success_url = reverse_lazy('documentos_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Documento eliminado correctamente.')
        return super().delete(request, *args, **kwargs)

# --- Bitacora Views ---
class BitacoraListView(LoginRequiredMixin, ListView):
    model = Bitacora
    template_name = 'gestion/bitacora_list.html'
    context_object_name = 'registros'
    ordering = ['-fecha_hora']

# --- Capacitacion Views ---
from .models import Capacitacion

class CapacitacionListView(LoginRequiredMixin, ListView):
    model = Capacitacion
    template_name = 'gestion/capacitacion_list.html'
    context_object_name = 'capacitaciones'

class CapacitacionCreateView(LoginRequiredMixin, CreateView):
    model = Capacitacion
    template_name = 'gestion/capacitacion_form.html'
    fields = ['nombre', 'fecha', 'modalidad', 'certificacion', 'id_dependencia']
    success_url = reverse_lazy('capacitaciones_list')

    def form_valid(self, form):
        messages.success(self.request, 'Capacitación registrada correctamente.')
        return super().form_valid(form)

class CapacitacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Capacitacion
    template_name = 'gestion/capacitacion_form.html'
    fields = ['nombre', 'fecha', 'modalidad', 'certificacion', 'id_dependencia']
    success_url = reverse_lazy('capacitaciones_list')

    def form_valid(self, form):
        messages.success(self.request, 'Capacitación actualizada correctamente.')
        return super().form_valid(form)

class CapacitacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Capacitacion
    template_name = 'gestion/capacitacion_confirm_delete.html'
    success_url = reverse_lazy('capacitaciones_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Capacitación eliminada correctamente.')
        return super().delete(request, *args, **kwargs)
