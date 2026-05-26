from django import forms

from casos.models import Caso_atencion
from usuarios.models import Usuario

class CasoBaseForm(forms.ModelForm):
    class Meta:
        model = Caso_atencion
        fields = []
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'desc_hechos': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Breve explicación de lo sucedido',
                'rows': 4
            }),
            #'tipo': forms.Select(attrs={'class': 'form-control'}),
            #'jerarquia_acoso': forms.Select(attrs={'class': 'form-control'}),
            'denunciante': forms.Select(attrs={'class': 'form-control'}),
            'denunciado': forms.Textarea(attrs={'class': 'form-control'}),
            'puesto_denunciado': forms.Textarea(attrs={'class': 'form-control'}),
            'dependencia_denunciado': forms.Select(attrs={'class': 'form-control'}),
            'direccion_hechos': forms.Textarea({'class': "form-control"}),
            'medidas_porteccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'persona_consejera': forms.Select(attrs={'class': 'form-control'}),
            'resolucion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'acta_cierre': forms.FileInput(attrs={
                'type': 'file',
                'class': 'form-control',
            })
        }

        labels = {
            'fecha': 'Fecha de los hechos',
            'desc_hechos': 'Descripción de los hechos',
            'persona_consejera': 'Vocal',
            'puesto_denunciado': 'Puesto del denunciado',
            'dependencia_denunciado': 'Dependencia del denunciado',
            'direccion_hechos': 'Dirección de los hechos',
            'medidas_proteccion': 'Medidas de protección tomadas',
            'resolucion': 'Resolución del caso',
            'acta_cierre': 'Acta de cierre',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if 'denunciado' in self.fields:
            self.fields['denunciado'].empty_label = "Prefiero no contestar"

        if 'persona_consejera' in self.fields:
            self.fields['persona_consejera'].queryset = Usuario.objects.select_related('id_rol').filter(id_rol_id=2)
            self.fields['persona_consejera'].empty_label = "Asignar vocal"

class CasoCreateFormAdmin(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = [
            #'tipo',
            #'jerarquia_acoso',
            'fecha',
            #'denunciante',
            'denunciado',
            'desc_hechos',
            'medidas_proteccion',
            'persona_consejera',
        ]

class CasoCreateFormVocal(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = [
            #'tipo',
            #'jerarquia_acoso',
            'fecha',
            #'denunciante',
            'denunciado',
            'desc_hechos',
        ]

class CasoCreateFormGeneral(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = [
            #'tipo',
            #'jerarquia_acoso',
            'fecha',
            #'denunciante',
            'denunciado',
            'desc_hechos',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.user = None
        if 'denunciante' in self.fields and self.user:
            self.fields['denunciante'].disabled = True
            self.fields['denunciante'].widget.attrs.update({
                'class': 'form-control',
                'readonly': 'readonly',
            })

            if hasattr(self.user, 'persona'):
                self.fields['denunciante'].initial = self.user.persona

class CasoUpdateForm(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = [ 'fecha', 'persona_consejera', 'resolucion']

class CasoCloseForm(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = ['acta_cierre', 'resolucion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['acta_cierre'].required = True
        self.fields['resolucion'].required = True

'''
Clases forms para renderizado de wizards
'''

OPTIONS = [(True, "Sí"), (False, "No")]

def coerse_boolean(x):
    return x == True

class PBaseForm(forms.ModelForm):
    class Meta:
        model = Caso_atencion
        fields = []

# Centro
class P1Form(PBaseForm):
    p1 = forms.TypedChoiceField(
        choices=OPTIONS,
        widget=forms.RadioSelect,
        coerce=coerse_boolean,
        label="¿Has experimentado situaciones en las que te has sentido insegura y/o en peligro?"
    )
    class Meta(PBaseForm.Meta):
        fields = ['p1']

class P2Form(PBaseForm):
    p2 = forms.TypedChoiceField(
        choices=OPTIONS,
        widget=forms.RadioSelect,
        coerce=coerse_boolean,
        label="¿Estas situaciones han ocurrido dentro del ámbito laboral?"
    )
    class Meta(PBaseForm.Meta):
        fields = ['p2']

# Izquierda
class P2_1Form(PBaseForm):
    p2_1 = forms.TypedChoiceField(
        choices=OPTIONS,
        widget=forms.RadioSelect,
        coerce=coerse_boolean,
        label="¿La persona que ha cometido estas acciones trabaja en la misma dependencia?"
    )
    class Meta(PBaseForm.Meta):
        fields = ['p2_1']

class P2_11Form(PBaseForm):
    p2_11 = forms.TypedChoiceField(
        choices=OPTIONS,
        widget=forms.RadioSelect,
        coerce=coerse_boolean,
        label="¿Los actos de molestia han sido por un superior"
    )
    class Meta(PBaseForm.Meta):
        fields = ['p2_11']

class CasoCreateFormSi(CasoBaseForm):
    class Meta(CasoCreateFormGeneral.Meta):
        fields = [
            'fecha',
            'denunciado',
            'puesto_denunciado',
            'desc_hechos',
        ]

class CasoCreateFormNo(CasoBaseForm):
    class Meta(CasoCreateFormGeneral.Meta):
        fields = [
            'fecha',
            'denunciado',
            'puesto_denunciado',
            'dependencia_denunciado',
            'desc_hechos',
        ]

# Derecha
class P2_2Form(PBaseForm):
    class Meta(PBaseForm.Meta):
        widgets = {
            'p2_2': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'p2_2': "¿En qué ámbito de tu vida ha sucedido?",
        }

class CasoCreateFormCF(CasoBaseForm):
    class Meta(CasoCreateFormGeneral.Meta):
        fields = [
            'fecha',
            'denunciado',
            'desc_hechos',
            # TODO: Nivel de parentesco
        ]

class CasoCreateFormCS(CasoBaseForm):
    class Meta(CasoCreateFormGeneral.Meta):
        fields = [
            'fecha',
            'denunciado',
            'desc_hechos',
        ]

class CasoCreateFormOtro(CasoBaseForm):
    class Meta(CasoCreateFormGeneral.Meta):
        fields = [
            'fecha',
            'direccion_hechos',
            'desc_hechos',
        ]