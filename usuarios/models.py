from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class Rol(models.Model):
    roles = [
        ('ADMIN', 'Administrador'),
        ('CAS', 'Comité de atención y seguimiento'),
        ('PC', 'Persona consejera'),
        ('CUG', 'Coordinación de unidad de género'),
        ('RH', 'Recursos humanos'),
        ('PG', 'Personal general'),
    ]

    PERMISOS_ROL =  {
        # Tiene acceso total al sistema
        'ADMIN': {
            'ver': ['personas', 'acciones', 'expedientes', 'bitacoras', 'capacitaciones', 'indicadores', 'usuarios'],
            'modificar': ['personas', 'acciones', 'expedientes', 'capacitaciones', 'indicadores', 'usuarios']
        },

        # Puede hacer consultas y modificaciones en general
        'CAS': {
            'ver': ['personas', 'acciones', 'expedientes', 'bitacoras', 'capacitaciones', 'indicadores'],
            'modificar': ['acciones', 'expedientes', 'capacitaciones']
        },

        # Solo puede hacer consultas y modificaciones de expedientes asignados
        'PC': {
            'ver': ['personas', 'acciones', 'expedientes', 'bitacoras'],
            'modificar': ['acciones', 'expedientes']
        },

        # No tiene acceso a contenido confidencial de expedientes
        'CUG': {
            'ver': ['personas', 'capacitaciones', 'indicadores'],
            'modificar': ['capacitaciones', 'indicadores']
        },

        # solo puede ver resoluciones finales de los expedientes, no los modifica
        'RH': {
            'ver': ['personas', 'capacitaciones', 'indicadores', 'expedientes'],
            'modificar': ['personas', 'capacitaciones'],
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
        return seccion in self.PERMISOS_ROL.get(self.nombre_rol, {}).get('modificaciones', [])

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

    def es_cas(self):
        return self.id_rol and self.id_rol.nombre_rol == 'CAS'

    def es_pc(self):
        return self.id_rol and self.id_rol.nombre_rol == 'PC'

    def es_cug(self):
        return self.id_rol and self.id_rol.nombre_rol == 'CUG'

    def es_pg(self):
        return self.id_rol and self.id_rol.nombre_rol == 'PG'

    @property
    def is_staff(self):
        return self.is_admin


