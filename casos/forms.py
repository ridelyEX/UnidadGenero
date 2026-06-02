from django import forms

from casos.models import CasoAtencion, CasoAtencionFlow, CasoAtencionDetails
from usuarios.models import Usuario

class CasoBaseForm(forms.ModelForm):
    desc_hechos = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Breve explicación de lo sucedido', 'rows': 4}),
        label='Descripción de los hechos',
        required=False
    )
    medidas_proteccion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Medidas de protección tomadas',
        required=False
    )
    direccion_hechos = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Dirección de los hechos',
        required=False
    )
    resolucion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Resolución del caso',
        required=False
    )
    acta_cierre = forms.FileField(
        widget=forms.FileInput(attrs={'type': 'file', 'class': 'form-control'}),
        label='Acta de cierre',
        required=False
    )
    class Meta:
        model = CasoAtencion
        fields = []
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'denunciante': forms.Select(attrs={'class': 'form-control'}),
            'denunciado': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto_denunciado': forms.TextInput(attrs={'class': 'form-control'}),
            'dependencia_denunciado': forms.Select(attrs={'class': 'form-control'}),
            'persona_consejera': forms.Select(attrs={'class': 'form-control'}),
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
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        requested_fields = getattr(self.Meta, 'fields', [])

        if requested_fields != '__all__' and requested_fields:
            # Identificamos qué campos "extra" definimos en la clase Base
            campos_extra = ['desc_hechos', 'medidas_proteccion', 'direccion_hechos', 'resolucion', 'acta_cierre']

            # Revisamos todos esos campos extra y si NO están en los "fields" de la subclase...
            for campo in campos_extra:
                if campo in self.fields and campo not in requested_fields:
                    # ¡Lo borramos para que no estorbe en el HTML!
                    del self.fields[campo]

        if instance and instance.pk:
            if hasattr(instance, 'detalles'):
                if 'desc_hechos' in self.fields:
                    self.fields['desc_hechos'].initial = instance.detalles.desc_hechos
                if 'medidas_proteccion' in self.fields:
                    self.fields['medidas_proteccion'].initial = instance.detalles.medidas_proteccion
                if 'resolucion' in self.fields:
                    self.fields['resolucion'].initial = instance.detalles.resolucion
                if 'acta_cierre' in self.fields:
                    self.fields['acta_cierre'].initial = instance.detalles.acta_cierre
            # Flow
            if hasattr(instance, 'flujo') and 'direccion_hechos' in self.fields:
                self.fields['direccion_hechos'].initial = instance.flujo.direccion_hechos


        if 'denunciado' in self.fields:
            self.fields['denunciado'].empty_label = "Prefiero no contestar"
        if 'persona_consejera' in self.fields:
            self.fields['persona_consejera'].queryset = Usuario.objects.select_related('id_rol').filter(id_rol_id=2)
            self.fields['persona_consejera'].empty_label = "Asignar vocal"

    def save(self, commit=True):
        # 3. Guardar el caso principal y redirigir los campos ajenos a sus tablas correctas
        caso = super().save(commit=False)
        if commit:
            caso.save()

            # Guardamos la parte de Detalles
            detalles, _ = CasoAtencionDetails.objects.get_or_create(caso=caso)
            if 'desc_hechos' in self.cleaned_data:
                detalles.desc_hechos = self.cleaned_data['desc_hechos']
            if 'medidas_proteccion' in self.cleaned_data:
                detalles.medidas_proteccion = self.cleaned_data['medidas_proteccion']
            if 'resolucion' in self.cleaned_data:
                detalles.resolucion = self.cleaned_data['resolucion']
            if self.cleaned_data.get('acta_cierre'):
                detalles.acta_cierre = self.cleaned_data['acta_cierre']
            detalles.save()

            # Guardamos la parte de Flujo (para direccion_hechos, que marcaste en tu modelo Flow)
            flujo, _ = CasoAtencionFlow.objects.get_or_create(caso=caso)
            if 'p1' in self.cleaned_data:
                flujo.p1 = self.cleaned_data['p1']
            if 'p2' in self.cleaned_data:
                flujo.p2 = self.cleaned_data['p2']
            if 'p2_1' in self.cleaned_data:
                flujo.p2_1 = self.cleaned_data['p2_1']
            if 'p2_11' in self.cleaned_data:
                flujo.p2_11 = self.cleaned_data['p2_11']
            if 'p2_2' in self.cleaned_data:
                flujo.p2_2 = self.cleaned_data['p2_2']
            if 'direccion_hechos' in self.cleaned_data:
                flujo.direccion_hechos = self.cleaned_data['direccion_hechos']
            flujo.save()

        return caso

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

OPTIONS = [('True', "Sí"), ('False', "No")]

def coerse_boolean(x):
    return x == 'True'

class PBaseForm(forms.ModelForm):
    class Meta:
        model = CasoAtencion
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
        label="¿Los actos de molestia han sido por un superior?"
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
    p2_2 = forms.ChoiceField(
        choices=CasoAtencion.ambito_choices,  # Importante: asegurarte de referenciar tus choices del modelo
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="¿En qué ámbito de tu vida ha sucedido?",
        required=False  # Opcional: Define si es requerido o no
    )
    class Meta(PBaseForm.Meta):
        fields = ['p2_2']
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