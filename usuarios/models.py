from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class Rol(models.Model):
    roles = [
        ('ADMIN', 'Administrador'),
        ('COORD', 'Coordinador'),
        ('VOC', 'Vocal'),
        ('SEC', 'Secretaria'),
        ('PG', 'Personal general'),
    ]

    PERMISOS_ROL =  {
        # Tiene acceso total al sistema
        'ADMIN': {
            'ver': ['personas', 'acciones', 'expedientes', 'bitacoras', 'capacitaciones', 'indicadores', 'usuarios'],
            'modificar': ['personas', 'acciones', 'expedientes', 'capacitaciones', 'indicadores', 'usuarios']
        },

        # Puede hacer consultas y modificaciones en general
        'COORD': {
            'ver': ['personas', 'acciones', 'expedientes', 'bitacoras', 'capacitaciones', 'indicadores'],
            'modificar': ['expedientes', 'capacitaciones', 'indicadores']
        },

        # Solo puede hacer consultas y modificaciones de expedientes asignados
        'VOC': {
            'ver': ['acciones', 'expedientes', 'bitacoras', 'capacitacione', 'indicadores'],
            'modificar': ['acciones', 'expedientes', 'indicadores']
        },

        # No tiene acceso a contenido confidencial de expedientes
        'SEC': {
            'ver': ['acciones', 'expedientes', 'bitacoras', 'capacitaciones', 'indicadores'],
            'modificar': ['expedientes', 'capacitaciones', 'indicadores']
        },

        # Solo puede consultar y crear su propio expediente. Verificar si puede consultar acciones
        'PG': {
            'ver': ['capacitaciones', 'expedientes'], #acciones
            'modificar': ['expedientes']
        }
    }

    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_rol

    def puede_ver(self, seccion):
        return seccion in self.PERMISOS_ROL.get(self.nombre_rol, {}).get('ver', [])

    def puede_modificar(self, seccion):
        return seccion in self.PERMISOS_ROL.get(self.nombre_rol, {}).get('modificar', [])

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es requerido')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es requerido')
        correo = self.normalize_email(correo)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True, help_text="Used as username")
    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    persona = models.OneToOneField('organizaciones.Persona', on_delete=models.CASCADE, null=True, blank=True, related_name='usuario')
    # ultimo_acceso is handled by AbstractBaseUser.last_login

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return f"{self.nombre}"

    def tiene_permiso_ver(self, seccion):
        if self.is_admin:
            return True
        if self.id_rol:
            return self.id_rol.puede_ver(seccion)
        return False

    def tiene_permiso_modificar(self, seccion):
        if self.is_admin:
            return True
        if self.id_rol:
            return self.id_rol.puede_modificar(seccion)
        return False

    def es_coordinador(self):
        return self.id_rol and self.id_rol.nombre_rol == 'COORD'

    def es_vocal(self):
        return self.id_rol and self.id_rol.nombre_rol == 'VOC'

    def es_secretaria(self):
        return self.id_rol and self.id_rol.nombre_rol == 'SEC'

    def es_pg(self):
        return self.id_rol and self.id_rol.nombre_rol == 'PG'

    @property
    def is_staff(self):
        return self.is_admin


