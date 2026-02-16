from django.db import models

class Persona(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    departamentos = [
        ('CIU', 'Departamento de infraestructura urbana'),
        ('CIS', 'Departamento de infraestructura social'),
        ('EYP', 'Departamento de estudios y proyectos'),
        ('MVI', 'Departamento de mantenimiento vial e  infraestructura'),
        ('SAOP', 'Departamento de servicios administrativos obras públicas'),
        ('TPG', 'Departamento de topografía'),
        ('JYA', 'Departamento de jurídico y afecciones'),
        ('LCO', 'Departamento de licitaciones y control de obra'),
        ('MPOP', 'Departamento de maquinaria pesada y obras públicas'),
        ('SIS', 'Despacho del subdirector de infraestructura social'),
        ('SIU', 'Despacho del subdirector de infraestructura urbana'),
        ('DOP', 'Despacho del director de obras públicas'),
    ]

    puestos = [
        ('ASR', 'Asesor A'),
        ('AUX', 'Auxiliar'),
        ('AUXE', 'Auxiliar especializado'),
        ('CDD', 'Capturista de datos'),
        ('CRAU', 'Chofer recolector de aseo urbano'),
        ('CJO', 'Consultor jurídico'),
        ('DGE', 'Director general'),
        ('JDD', 'Jefe de departamento'),
        ('JDDI', 'Jefe de división'),
        ('JDO', 'Jefe de oficina'),
        ('LDP', 'Líder de proyecto'),
        ('MEC', 'Mecánico'),
        ('OPS', 'Operador de servicio 6'),
        ('PES', 'Personal especializado'),
        ('RDO', 'Residente de obra'),
        ('SUB', 'Subdirector'),
        ('SDO', 'Supervisor de obra'),
        ('SDS', 'Supervisor de servicios'),
        ('TEA', 'Técnico especializado administrativo'),
        ('TSO', 'Técnico servicios y operaciones'),
        ('TVG', 'Técnico vigilante'),
    ]

    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    curp = models.CharField(max_length=18, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    cargo = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100, choices=puestos, blank=True, null=True)
    departamento = models.CharField(max_length=100, choices=departamentos, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
