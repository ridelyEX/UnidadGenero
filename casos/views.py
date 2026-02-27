from hmac import new
import logging
from django import forms
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Caso_atencion

logger = logging.getLogger(__name__)

# Mixin para requerir que el usuario sea administrador
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

class CasoListView(AdminRequiredMixin, ListView):
    model = Caso_atencion
    template_name = 'casos/caso_list.html'
    context_object_name = 'expedientes'

# Vista para crear un nuevo caso de atención, con generación automática de folio y manejo de jerarquía de acoso
class CasoCreateView(LoginRequiredMixin, CreateView):
    model = Caso_atencion
    template_name = 'casos/caso_form.html'
    fields = ['tipo', 'jerarquia_acoso', 'fecha', 'denunciante', 'denunciado', 'medidas_proteccion', 'persona_consejera',]
    success_url = reverse_lazy('expediente_list')

    def get_form_class(self):
        base_fields = ['tipo', 'jerarquia_acoso', 'fecha', 'denunciado']

        if self.request.user.id_rol or (self.request.user.id_rol and self.request.user.id_rol.nombre_rol == 'CAS'):
            self.fields = base_fields + ['denunciante', 'medidas_proteccion', 'persona_consejera']
        elif self.request.user.id_rol and self.request.user.id_rol.nombre_rol == 'PC':
            self.fields = base_fields + ['denunciante']
        else:
            self.fields = base_fields + ['denunciante']

        return super().get_form_class()

    ### Sobrescribir el método get_form para usar un widget de fecha
    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        form.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})

        if 'persona_consejera' in form.fields:
            from usuarios.models import Usuario
            queryset = Usuario.objects.select_related('id_rol').filter(id_rol_id=2)
            logger.info(f"Usuarios que son personas consejeras: {queryset.count()}")
            form.fields['persona_consejera'].queryset = queryset

            form.fields['persona_consejera'].empty_label = "Asignar consejero(a)"
            form.fields['persona_consejera'].widget.attrs.update({'class': 'form-control'})

        return form

    ### Sobrescribir el método form_valid para generar folio único y manejar jerarquía de acoso
    def form_valid(self, form):
        # Generar folio único basado en el tipo de caso
        form.instance.folio = self.folio(form.instance.tipo)
        # Si el tipo no es ACL, establecer jerarquía de acoso como 'N/A'
        if form.instance.tipo != 'ACL':
            form.instance.jerarquia_acoso = 'N/A'

        if form.instance.persona_consejera:
            form.instance.estatus = 'En Proceso'
            logger.info(f"Caso creado con estatus 'En Proceso'")
        else:
            logger.info(f"Caso creado con estatus 'Abierto'")

        messages.success(self.request, 'Expediente registrado exitosamente.')
        return super().form_valid(form)

    ### Método para generar folio único basado en el tipo de caso
    def folio(self, tipo):
        last_caso = Caso_atencion.objects.order_by('id_caso').last()
        if last_caso and last_caso.folio and last_caso.folio.startswith('CASO-'):
            try:
                last_number= int(last_caso.folio.split('-')[2])
                new_number = last_number + 1
            except (IndexError, ValueError):
                new_number = 1
        else:
            new_number = 1
        return f'CASO-{tipo}-{new_number:04d}'

class CasoUpdateView(AdminRequiredMixin, UpdateView):
    model = Caso_atencion
    template_name = 'casos/caso_form.html'
    fields = ['tipo', 'fecha', 'persona_consejera', 'resolucion']
    success_url = reverse_lazy('expediente_list')

    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        form.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'})

        if 'persona_consejera' in form.fields:
            from usuarios.models import Usuario
            queryset = Usuario.objects.select_related('id_rol').filter(id_rol_id=2)
            logger.info(f"Personas consejeras encontradas: {queryset.count()}")
            form.fields['persona_consejera'].queryset = queryset

            form.fields['persona_consejera'].empty_label = "Asignar consejero(a)"
            form.fields['persona_consejera'].widget.attrs.update({'class': 'form-control'})

        return form

    def status_change(self):
        caso = self.object

        if caso.persona_consejera and caso.estatus == 'Abierto':
            caso.estatus = 'En Proceso'
            logger.info(f"Estatus del caso cambiado")
            return 'En Proceso'

        logger.debug(f"El estatus no fue cambiado")
        return caso.estatus

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.status_change()

        self.object.save()

        messages.success(self.request, 'Expediente actualizado exitosamente.')
        return super().form_valid(form)

class CasoCloseView(AdminRequiredMixin, UpdateView):
    model = Caso_atencion
    template_name = 'casos/caso_close.html'
    fields = ['acta_cierre', 'resolucion']
    success_url = reverse_lazy('expediente_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['acta_cierre'].widget = forms.FileInput(attrs={'type': 'file', 'class': 'form-control'})
        form.fields['resolucion'].widget = forms.Textarea(attrs={'class': 'form-control'})
        return form

    def status_change(self):
        caso = self.object

        if caso.persona_consejera and caso.estatus == 'En Proceso' and caso.acta_cierre and caso.resolucion:
            caso.estatus = 'Cerrado'
            logger.info(f"Expediente cerrado")
            return 'Cerrado'

        logger.debug(f"El expediente no fue cerrado")
        return caso.estatus

    def close_date(self):
        caso = self.object

        if caso.persona_consejera and caso.estatus == 'Cerrado':
            caso.fecha_cierre = timezone.now()
            logger.info(f"Fecha de cierre: {caso.fecha_cierre}")
            return caso.fecha_cierre

        logger.debug(f"No hay fecha de cierre asignada")
        return caso.fecha_cierre

    def form_valid(self, form):

        self.object = form.save(commit=False)

        # Cambia el estado del caso a cerrado
        self.status_change()
        # Asigna la fecha de cierre del caso
        self.close_date()

        self.object.save()

        messages.success(self.request, 'Expediente cerrado.')
        return super().form_valid(form)

class CasoDeleteView(AdminRequiredMixin, DeleteView):
    model = Caso_atencion
    template_name = 'casos/caso_confirm_delete.html'
    success_url = reverse_lazy('expediente_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Expediente eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
