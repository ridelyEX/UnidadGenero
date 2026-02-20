from functools import wraps

from django.core.exceptions import PermissionDenied


def require_permiso_ver(seccion):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.tiene_permiso_ver(seccion):
                raise PermissionDenied("No tienes permiso para ver esta sección")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_permiso_modificar(seccion):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.tiene_permiso_modificar(seccion):
                raise PermissionDenied("No tienes permiso para modificar esta sección")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator