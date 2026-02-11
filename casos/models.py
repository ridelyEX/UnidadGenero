from django.db import models

class Caso_atencion(models.Model):
    id_caso = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    fecha = models.DateField()
    estatus = models.CharField(max_length=50) # Abierto, Cerrado, En Proceso
    medidas = models.TextField()

    def __str__(self):
        return f"Caso {self.id_caso} - {self.tipo}"
