from django.db import models

class Dependencia(models.Model):
    id_dependencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    cargo = models.CharField(max_length=100)
    id_dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
