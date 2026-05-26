from django.contrib.sessions.management.commands import clearsessions
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from .forms import (
    P1Form, P2Form, P2_1Form, P2_11Form, P2_2Form,
    CasoCreateFormSi, CasoCreateFormNo, CasoCreateFormCF, CasoCreateFormCS, CasoCreateFormOtro
)
from .models import Caso_atencion

FORMS = [
    ('p1', P1Form),
    ('p2', P2Form),
    # Izquierda
    ('p2_1', P2_1Form),
    ('p2_11', P2_11Form),
    ('caso_si', CasoCreateFormSi),
    ('caso_no', CasoCreateFormNo),
    # Derecha
    ('p2_2', P2_2Form),
    ('caso_cf', CasoCreateFormCF),
    ('caso_cs', CasoCreateFormCS),
    ('caso_otro', CasoCreateFormOtro),
]

def is_left(wizard):
    '''Muestra rama izquierda si p2 es true'''
    cleaned_data = wizard.get_cleaned_data_for_step("p2") or {}
    return cleaned_data.get("p2") is True

def show_p2_11(wizard):
    return is_left(wizard)

def show_caso_si(wizard):
    '''Muestra la pregunta p2_11 si es true'''
    if not is_left(wizard): return False
    cleaned_data = wizard.get_cleaned_data_for_step("p2_11") or {}
    return cleaned_data.get("p2_11") is True

def show_caso_no(wizard):
    '''Muestra la pregunt a p2_11 es false'''
    if not is_left(wizard): return False
    cleaned_data = wizard.get_cleaned_data_for_step("p2_11") or {}
    return cleaned_data.get("p2_11") is False

# Derecha
def is_right(wizard):
    '''Muestra rama derecha si p2 es false'''
    cleaned_data = wizard.get_cleaned_data_for_step("p2") or {}
    return cleaned_data.get("p2") is False

def show_caso_cf(wizard):
    if not is_right(wizard): return False
    cleaned_data = wizard.get_cleaned_data_for_step("p2_2") or {}
    return cleaned_data.get("p2_2") == 'CF'

def show_caso_cs(wizard):
    if not is_right(wizard): return False
    cleaned_data = wizard.get_cleaned_data_for_step("p2_2") or {}
    return cleaned_data.get("p2_2") == 'CS'

def show_caso_otro(wizard):
    if not is_right(wizard): return False
    cleaned_data = wizard.get_cleaned_data_for_step("p2_2") or {}
    return cleaned_data.get("p2_2") == 'Otro'

CONDITIONS = {
    # Izquierda
    'p2_1': is_left,
    'p2_11': show_p2_11,
    'caso_si': show_caso_si,
    'caso_no': show_caso_no,

    # Derecha
    'p2_2': is_right,
    'caso_cf': show_caso_cf,
    'caso_cs': show_caso_cs,
    'caso_otro': show_caso_otro,
}

# Clases de wizards
class CreateCasoWizard(SessionWizardView):
    template_name = "casos/caso_wizard.html"

    def done(self, form_list, **kwargs):
        nuevo_caso = Caso_atencion()
        for form in form_list:
            for campo, valor in form.cleaned_data.items():
                setattr(nuevo_caso, campo, valor)

        nuevo_caso.creado_por = self.request.user
        nuevo_caso.save()

        return render(self.request, "", {"caso":nuevo_caso})