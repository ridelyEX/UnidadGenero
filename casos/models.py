from django.db import models
from django.db.models import SET_NULL

from unidad_genero import settings

class CasoAtencion(models.Model):
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
    # Folio único del caso
    folio = models.CharField(max_length=30, unique=True, null=True, blank=True)

    # Personas involucradas en el caso
    denunciante = models.ForeignKey('organizaciones.Persona', on_delete=SET_NULL, null=True, related_name='casos_denunciante')

    # Datos del denunciado
    denunciado = models.CharField(max_length=100, blank=True, null=True)
    dependencia_denunciado = models.ForeignKey('dependencias.Dependencias', on_delete=SET_NULL, null=True, related_name='casos_dependencia_denunciado')
    puesto_denunciado = models.CharField(max_length=100, blank=True, null=True)

    # Personal asignado al caso
    persona_consejera = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='casos_asignados')
    comite_resolutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='casos_resueltos')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='casos_creados')

    # Fecha de incidencia y cierre de expediente
    fecha = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    # Estatus del caso
    estatus = models.CharField(max_length=50, choices=estatus_choices, default='Abierto') # Abierto, Cerrado, En Proceso

    def __str__(self):
        return f"Caso {self.id_caso} - {self.tipo}"

class CasoAtencionFlow(models.Model):
    '''
    Tabla que controla el flujo de los wizards y almacena las respuestas a las preguntas de cada paso para cada caso de atención,
    permitiendo así tener un registro del proceso seguido en cada caso y facilitar la generación de reportes y análisis posteriores.
    '''
    caso = models.OneToOneField(CasoAtencion, on_delete=models.CASCADE, related_name="flujo")
    # Preguntas de flujo
    p1 = models.BooleanField(default=False)
    p2 = models.BooleanField(default=False)

    # Izquierda
    p2_1 = models.BooleanField(default=False)
    p2_11 = models.BooleanField(default=False)

    # Derecha
    p2_2 = models.CharField(blank=True, null=True, max_length=100, choices=Caso_atencion.ambito_choices)
    direccion_hechos = models.CharField(blank=True, null=True, max_length=150)


class CasoAtencionDetails(models.Model):
    '''
    TODO: Tabla secundaria del modelo Caso_atencion para separar los detalles de la base de datos y evitar sobrecarga
    '''
    caso = models.OneToOneField(CasoAtencion, on_delete=models.CASCADE, related_name="detalles")

    # Campo de descripción de hechos
    desc_hechos = models.TextField(max_length=500, blank=True, null=True)
    # Descripción de las medidas de protección tomadas
    medidas_proteccion = models.TextField(blank=True, null=True)
    resolucion = models.TextField(blank=True, null=True)
    acta_cierre = models.FileField(upload_to='actas/', verbose_name='actas', blank=True, null=True)

    def __str__(self):
        return f"Detalles del caso {self.caso}"


