from django.db import models

from casos.models import Caso_atencion


class Indicador(models.Model):
    id_indicador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=100) # Quantitativo, Qualitativo
    periodicidad = models.CharField(max_length=50) # Mensual, Anual

    casos = models.ManyToManyField(Caso_atencion, blank=True, related_name='indicadores')

    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
