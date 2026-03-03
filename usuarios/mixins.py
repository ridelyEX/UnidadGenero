# usuarios/mixins.py (NUEVO ARCHIVO)
from django.contrib.auth.mixins import UserPassesTestMixin


class RolRequiredMixin(UserPassesTestMixin):
    """Restringe acceso según roles permitidos"""
    roles_permitidos = ['ADMIN', 'COORD']

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_admin:
            return True
        if self.request.user.id_rol:
            return self.request.user.id_rol.nombre_rol in self.roles_permitidos
        return False

class PermisoVerMixin(UserPassesTestMixin):
    """Verifica permiso de ver según sección"""
    seccion = None

    def test_func(self):
        return self.request.user.tiene_permiso_ver(self.seccion)

class PermisoModificarMixin(UserPassesTestMixin):
    """Verifica permiso de modificar según sección"""
    seccion = None

    def test_func(self):
        return self.request.user.tiene_permiso_modificar(self.seccion)