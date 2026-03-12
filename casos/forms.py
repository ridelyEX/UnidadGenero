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
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'jerarquia_acoso': forms.Select(attrs={'class': 'form-control'}),
            'denunciante': forms.Select(attrs={'class': 'form-control'}),
            'denunciado': forms.Select(attrs={'class': 'form-control'}),
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
            'desc_hechos': 'Descripción de los hechos',
            'persona_consejera': 'Vocal',
        }

        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)

            if 'denunciado' in self.fields:
                self.fileds['denunciado'].empty_label = "Prefiero no contestar"

            if 'persona_consejera' in self.fields:
                self.fields['persona_consejera'].queryset = Usuario.objects.select_related('id_rol').filter(id_rol_id=2)
                self.fields['persona_consejera'].empty_label = "Asignar vocal"

class CasoCreateFormAdmin(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = [
            'tipo',
            'jerarquia_acoso',
            'fecha',
            'denunciante',
            'denunciado',
            'desc_hechos',
            'medidas_proteccion',
            'persona_consejera',
        ]

class CasoCreateFormVocal(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = [
            'tipo',
            'jerarquia_acoso',
            'fecha',
            'denunciante',
            'denunciado',
            'desc_hechos',
        ]

class CasoCreateFormGeneral(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = [
            'tipo',
            'jerarquia_acoso',
            'fecha',
            'denunciante',
            'denunciado',
            'desc_hechos',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'denunciante' in self.fields and self.user:
            self.fields['denunciante'].disabled = True
            self.fields['denunciante'].widgets.attrs.update({
                'class': 'form-control',
                'readonly': 'readonly',
            })

            if hasattr(self.user, 'persona'):
                self.fields['denunciante'].initial = self.user.persona

class CasoUpdateForm(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = ['tipo', 'fecha', 'persona_consejera', 'resolucion']

class CasoCloseForm(CasoBaseForm):
    class Meta(CasoBaseForm.Meta):
        fields = ['acta_cierre', 'resolucion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['acta_cierre'].required = True
        self.fields['resolucion'].required = True