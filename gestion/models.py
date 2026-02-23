from django.db import models
from django.conf import settings

from casos.models import Caso_atencion
from organizaciones.models import Persona


class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    tipo_actividad = models.CharField(max_length=100)
    objetivo = models.TextField()
    fecha_inicio = models.DateField()
    estatus = models.CharField(max_length=50)
    id_usuario_responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='actividades_responsable')

    def __str__(self):
        return f"{self.tipo_actividad} - {self.objetivo[:50]}"

class Bitacora(models.Model):
    id_bitacora = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=200)
    observaciones = models.TextField()
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    id_actividades = models.ForeignKey(Actividad, on_delete=models.CASCADE)

    caso = models.ForeignKey(Caso_atencion, on_delete=models.CASCADE, related_name='bitacoras', null=True, blank=True)

    editable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.accion} - {self.fecha_hora}"

class Documento(models.Model):
    # Tipo de documentos
    tipo_documentos = [
        ('MIN', 'Minutas'),
        ('CDC', 'Constancias de capacitación'),
        ('ETV', 'Entrevistas'),
        ('TPL', 'Test psicológico'),
        ('TPM', 'Test piscométrico'),
        ('CVT', 'Convocatoria'),
        ('EVD', 'Evidencias'),
    ]

    # Información del documento
    id_documento = models.AutoField(primary_key=True)
    nombre_archivo = models.CharField(max_length=200)
    tipo_documento = models.CharField(max_length=100, choices=tipo_documentos)
    ruta_archivo = models.FileField(upload_to='documentos/')
    fecha_carga = models.DateTimeField(auto_now_add=True)
    version = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=50)

    # Datos relacionados la documento
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    caso = models.ForeignKey(Caso_atencion, on_delete=models.CASCADE, null=True, blank=True, related_name='documentos')
    id_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, null=True, blank=True)

    # Confidencialidad del documento
    nivel_confidencialidad = models.CharField(
        max_length=20,
        choices=[
            ('ALTO', 'Alto'),
            ('MEDIO', 'Medio'),
            ('BAJO', 'Bajo')
        ],
        default='ALTO'
    )

    def __str__(self):
        return self.nombre_archivo

class Capacitacion(models.Model):
    id_capacitacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    fecha = models.DateField()
    modalidad = models.CharField(max_length=50) # Presencial, Virtual, Hibrida
    certificacion = models.BooleanField(default=False)

    participantes = models.ManyToManyField(Persona, related_name='capacitaciones')

    def __str__(self):
        return self.nombre
