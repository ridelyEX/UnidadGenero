from django.db import models

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
    ]

    id_caso = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100, choices=tipos_violencia)
    jerarquia_acoso = models.CharField(max_length=2, choices=jerarquias_acoso, blank=True, null=True, verbose_name="Jerarquía de Acoso")
    fecha = models.DateField()
    estatus = models.CharField(max_length=50, choices=estatus_choices) # Abierto, Cerrado, En Proceso
    medidas = models.TextField()

    def __str__(self):
        return f"Caso {self.id_caso} - {self.tipo}"
