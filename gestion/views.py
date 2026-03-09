from django import forms
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from casos.mixins import VocalOSuperiorMixin
from usuarios.mixins import PermisoVerMixin, PermisoModificarMixin, RolRequiredMixin
from .models import Actividad, Documento, Bitacora

# --- Actividad Views ---
class ActividadListView(PermisoVerMixin, ListView):
    model = Actividad
    template_name = 'gestion/actividad_list.html'
    context_object_name = 'actividades'

class ActividadCreateView(PermisoModificarMixin, CreateView):
    model = Actividad
    template_name = 'gestion/actividad_form.html'
    fields = ['id_caso', 'tipo_actividad', 'objetivo', 'fecha_inicio', 'id_usuario_responsable']
    success_url = reverse_lazy('actividades_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Personalizar etiquetas y widgets
        form.fields['tipo_actividad'].label = 'Tipo de actividad'

        # Personalizar el campo de fecha para usar un selector de fecha
        form.fields['fecha_inicio'].label = 'Fecha de inicio'
        form.fields['fecha_inicio'].widget = forms.DateInput(attrs={'type': 'date'})
        form.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})

        # Personalizar el campo de caso para mostrar el folio en lugar del ID
        form.fields['id_caso'].label = 'Folio del caso'
        form.fields['id_caso'].empty_label = 'Seleccionar folio del caso'
        form.fields['id_caso'].label_from_instance = lambda obj: f"{obj.folio}"

        # Personalizar el campo de usuario responsable para mostrar el nombre completo
        form.fields['id_usuario_responsable'].label = 'Usuario responsable'

        return form

    def form_valid(self, form):
        messages.success(self.request, 'Actividad creada correctamente.')
        return super().form_valid(form)

class ActividadUpdateView(PermisoModificarMixin, UpdateView):
    model = Actividad
    template_name = 'gestion/actividad_form.html'
    fields = ['tipo_actividad', 'objetivo', 'fecha_inicio','id_usuario_responsable']
    success_url = reverse_lazy('actividades_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['fecha_inicio'].label = 'Fecha de inicio'
        form.fields['fecha_inicio'].widget = forms.DateInput(attrs={'type': 'date'})
        form.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})

        return form

    def form_valid(self, form):
        messages.success(self.request, 'Actividad actualizada correctamente.')
        return super().form_valid(form)

class ActividadDeleteView(RolRequiredMixin, DeleteView):
    model = Actividad
    template_name = 'gestion/actividad_confirm_delete.html'
    success_url = reverse_lazy('actividades_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Actividad eliminada correctamente.')
        return super().delete(request, *args, **kwargs)

# --- Documento Views ---
class DocumentoListView(PermisoVerMixin, ListView):
    model = Documento
    template_name = 'gestion/documento_list.html'
    context_object_name = 'documentos'

class DocumentoCreateView(PermisoModificarMixin, CreateView):
    model = Documento
    template_name = 'gestion/documento_form.html'
    fields = ['nombre_archivo', 'tipo_documento', 'ruta_archivo', 'version', 'estado', 'id_actividad']
    success_url = reverse_lazy('documentos_list')

    def form_valid(self, form):
        form.instance.id_usuario = self.request.user
        messages.success(self.request, 'Documento subido correctamente.')
        return super().form_valid(form)

class DocumentoDeleteView(RolRequiredMixin, DeleteView):
    model = Documento
    template_name = 'gestion/documento_confirm_delete.html'
    success_url = reverse_lazy('documentos_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Documento eliminado correctamente.')
        return super().delete(request, *args, **kwargs)



# --- Bitacora Views ---
class BitacoraListView(PermisoVerMixin, ListView):
    model = Bitacora
    template_name = 'gestion/bitacora_list.html'
    context_object_name = 'registros'
    ordering = ['-fecha_hora']

# --- Capacitacion Views ---
from .models import Capacitacion

class CapacitacionListView(PermisoVerMixin, ListView):
    model = Capacitacion
    template_name = 'gestion/capacitacion_list.html'
    context_object_name = 'capacitaciones'

class CapacitacionCreateView(PermisoModificarMixin, CreateView):
    model = Capacitacion
    template_name = 'gestion/capacitacion_form.html'
    fields = ['nombre', 'responsable', 'fecha_inicio', 'fecha_fin', 'tipo_actividad', 'tema', 'objetivo', 'materiales', 'participantes']
    success_url = reverse_lazy('capacitaciones_list')

    def get_form(self, form_class = None):
        form = super().get_form(form_class)

        form.fields['nombre'].label = 'Nombre de la capacitación'

        form.fields['responsable'].label = 'Responsable de la capacitación'

        form.fields['fecha_inicio'].label = 'Fecha de inicio'
        form.fields['fecha_inicio'].widget = forms.DateInput(attrs={'type': 'date'})
        form.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})

        form.fields['fecha_fin'].label = 'Fecha de conclusión'
        form.fields['fecha_fin'].widget = forms.DateTimeInput(attrs={'type': 'date'})
        form.fields['fecha_fin'].widget.attrs.update({'class': 'form-control'})

        form.fields['tipo_actividad'].label = 'Tipo de capacitación'

        form.fields['tema'].label = 'Tema de la capacitación'

        return form

    def form_valid(self, form):
        messages.success(self.request, 'Capacitación registrada correctamente.')
        return super().form_valid(form)

class CapacitacionUpdateView(PermisoModificarMixin, UpdateView):
    model = Capacitacion
    template_name = 'gestion/capacitacion_form.html'
    fields = ['nombre', 'fecha', 'modalidad', 'certificacion']
    success_url = reverse_lazy('capacitaciones_list')

    def form_valid(self, form):
        messages.success(self.request, 'Capacitación actualizada correctamente.')
        return super().form_valid(form)

class CapacitacionDeleteView(RolRequiredMixin, DeleteView):
    model = Capacitacion
    template_name = 'gestion/capacitacion_confirm_delete.html'
    success_url = reverse_lazy('capacitaciones_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Capacitación eliminada correctamente.')
        return super().delete(request, *args, **kwargs)
