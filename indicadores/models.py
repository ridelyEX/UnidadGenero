from django.db import models

class Indicador(models.Model):
    id_indicador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=100) # Quantitativo, Qualitativo
    periodicidad = models.CharField(max_length=50) # Mensual, Anual
    fecha = models.DateField()

    def __str__(self):
        return self.nombre
