from django.db import models
from django.db.models import SET_NULL

from unidad_genero import settings


class Caso_atencion(models.Model):
    tipos_violencia = [
        ('VLG', 'Violencia laboral general'),
        ('ACL', 'Acoso laboral'),
        ('HOM', 'Hostigamiento sexual'),
        ('ACS', 'Acoso sexual'),
        ('DCL', 'Discriminación laboral'),
        ('VRG', 'Violencia por razón de género'),
    ]

    estatus_choices = [
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado'),
        ('En Proceso', 'En Proceso'),
    ]

    jerarquias_acoso = [
        ('HO', 'Horizontal'),
        ('VD', 'Vertical descendente'),
        ('VA', 'Vertical ascendente'),
        ('N/A', 'No Aplica'),
    ]

    id_caso = models.AutoField(primary_key=True)

    # Personas involucradas en el caso
    denunciante = models.ForeignKey('organizaciones.Persona', on_delete=SET_NULL, null=True, related_name='casos_denunciante')
    denunciado = models.ForeignKey('organizaciones.Persona', on_delete=models.SET_NULL, null=True, related_name='casos_denunciado')

    # Personal asignado al caso
    persona_consejera = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='casos_asignados')
    # Persona que resuelve el caso, puede ser diferente a la persona consejera si el caso es escalado al comité de atención y seguimiento
    comite_resolutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='casos_resueltos')

    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='casos_creados')

    # Folio único del caso
    folio = models.CharField(max_length=30, unique=True, null=True, blank=True)

    # Tipo de violencia denunciada
    tipo = models.CharField(max_length=100, choices=tipos_violencia)
    jerarquia_acoso = models.CharField(max_length=5, choices=jerarquias_acoso, blank=True, default='N/A', verbose_name="Jerarquía de Acoso")
    # Descripción de las medidas de protección tomadas
    medidas_proteccion = models.TextField(blank=True, null=True)

    # Fecha de incidencia y cierre de expediente
    fecha = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    # Estatus del caso
    estatus = models.CharField(max_length=50, choices=estatus_choices, default='Abierto') # Abierto, Cerrado, En Proceso

    # Nivel de confidencialidad y medidas tomadas
    nivel_confidencialidad = models.CharField(max_length=20,
                                            choices=[
                                                    ('ALTO', 'alto'),
                                                    ('MEDIO', 'Medio'),
                                                    ('BAJO', 'Bajo')
                                                ],
                                                default='ALTO'
                                            )
    resolucion = models.TextField(blank=True, null=True)
    acta_cierre = models.FileField(upload_to='actas/', verbose_name='actas', blank=True, null=True)

    def __str__(self):
        return f"Caso {self.id_caso} - {self.tipo}"
