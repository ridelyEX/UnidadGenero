from django.db import models
from django.db.models import SET_NULL

from unidad_genero import settings

class Caso_atencion(models.Model):
    estatus_choices = [
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado'),
        ('En Proceso', 'En Proceso'),
    ]

    ambito_choices = [
        ('CF', 'Círculo familiar'),
        ('CS', 'Círculo social'),
        ('Otro', 'Otro'),
    ]

    id_caso = models.AutoField(primary_key=True)

    # Personas involucradas en el caso
    denunciante = models.ForeignKey('organizaciones.Persona', on_delete=SET_NULL, null=True, related_name='casos_denunciante')
    #denunciado = models.ForeignKey('organizaciones.Persona', on_delete=models.SET_NULL, null=True, related_name='casos_denunciado', default='Prefiero no contestar')

    denunciado = models.CharField(max_length=100, blank=True, null=True)

    # Personal asignado al caso
    persona_consejera = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='casos_asignados')
    # Persona que resuelve el caso, puede ser diferente a la persona consejera si el caso es escalado al comité de atención y seguimiento
    comite_resolutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='casos_resueltos')

    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='casos_creados')

    # Preguntas de flujo
    p1 = models.BooleanField(default=False)
    p2 = models.BooleanField(default=False)

    # Izquierda
    p2_1 = models.BooleanField(default=False)
    p2_11 = models.BooleanField(default=False)
    p2_12 = models.BooleanField(default=False)

    # Derecha
    p2_2 = models.CharField(blank=True, null=True, max_length=100, choices=ambito_choices)
    direccion_hechos = models.CharField(blank=True, null=True, max_length=150)

    # Folio único del caso
    folio = models.CharField(max_length=30, unique=True, null=True, blank=True)

    # Tipo de violencia denunciada
    #tipo = models.CharField(max_length=100, choices=tipos_violencia)
    #jerarquia_acoso = models.CharField(max_length=5, choices=jerarquias_acoso, blank=True, default='N/A', verbose_name="Jerarquía de Acoso")

    # Campo de descripción de hechos
    desc_hechos = models.TextField(max_length=500, blank=True, null=True)
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

class CasoAtencionFlow(models.Model):
    '''
    TODO: Seperacióon del modelo con tabla secundaria para facilidad de lectura y evitar sobrecarga en base de datos
    '''

class CasoAtencionDetails(models.Model):
    '''
    TODO: Tabla secundaria del modelo Caso_atencion para separar los detalles de la base de datos y evitar sobrecarga
    '''
