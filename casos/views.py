from hmac import new
import logging
from django import forms
from django.db import models
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import CasoCreateFormAdmin, CasoCreateFormVocal, CasoCreateFormGeneral
from .mixins import CoordinadorRequiredMixin, VocalOSuperiorMixin
from .models import Caso_atencion
from django.db.models import Q

logger = logging.getLogger(__name__)

# Mixin para requerir que el usuario sea administrador
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

class CasoListView(LoginRequiredMixin, ListView):
    model = Caso_atencion
    template_name = 'casos/caso_list.html'
    context_object_name = 'expedientes'

    def get_queryset(self):
        user = self.request.user

        if user.is_admin or user.es_coordinador():
            return Caso_atencion.objects.all()

        elif user.es_vocal() or user.es_secretaria():
            # return Caso_atencion.objects.filter(persona_consejera=user) query para listar casos asignados (no se asignan de momento)
            if hasattr(user, 'persona'):
                return Caso_atencion.objects.filter(
                    Q(persona_consejera=user) | Q(denunciante=user.persona)
                )
            else:
                return Caso_atencion.objects.filter(persona_consejera=user)

        else:
            if hasattr(user, 'persona'):
                return Caso_atencion.objects.filter(
                    models.Q(denunciante=user.persona) #| models.Q(denunciado=user.persona lista los expedientes en los que es señalado. En desuso
                )
            else:
                return Caso_atencion.objects.none()

# Vista para crear un nuevo caso de atención, con generación automática de folio y manejo de jerarquía de acoso
class CasoCreateView(LoginRequiredMixin, CreateView):
    model = Caso_atencion
    template_name = 'casos/caso_form.html'
    # fields = ['tipo', 'jerarquia_acoso', 'fecha', 'denunciante', 'denunciado', 'medidas_proteccion', 'persona_consejera',]
    success_url = reverse_lazy('expediente_list')

    def get_form_class(self):
        user = self.request.user
        if user.is_admin or user.es_coordinador():
            return CasoCreateFormAdmin
        elif user.es_vocal() or user.es_secretaria():
            return CasoCreateFormVocal
        else:
            return CasoCreateFormGeneral

    ### Sobrescribir el método get_form para usar un widget de fecha
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    ### Sobrescribir el método form_valid para generar folio único y manejar jerarquía de acoso
    def form_valid(self, form):
        # Generar folio único basado en el tipo de caso
        form.instance.folio = self.folio(form.instance.tipo)

        user = self.request.user
        if not (user.is_admin or user.es_coordinador()):
            if hasattr(user, 'persona'):
                form.instance.denunciante = user.persona
            else:
                messages.error(self.request, 'El usuario no tiene personal asignado')
                return self.form_invalid(form)

        form.instance.creado_por = user

        if form.instance.persona_consejera:
            form.instance.estatus = 'En Proceso'
            logger.info(f"Caso creado con estatus 'En Proceso'")
        else:
            form.instance.estatus = 'Abierto'
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

class CasoUpdateView(VocalOSuperiorMixin, UpdateView):
    model = Caso_atencion
    template_name = 'casos/caso_form.html'
    fields = ['tipo', 'fecha', 'persona_consejera', 'resolucion']
    success_url = reverse_lazy('expediente_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

class CasoCloseView(CoordinadorRequiredMixin, UpdateView):
    model = Caso_atencion
    template_name = 'casos/caso_close.html'
    fields = ['acta_cierre', 'resolucion']
    success_url = reverse_lazy('expediente_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

class CasoDeleteView(CoordinadorRequiredMixin, DeleteView):
    model = Caso_atencion
    template_name = 'casos/caso_confirm_delete.html'
    success_url = reverse_lazy('expediente_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Expediente eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
