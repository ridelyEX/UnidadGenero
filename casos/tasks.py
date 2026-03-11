import logging

from django.conf import settings
from django.core.mail import send_mail

from casos.models import Caso_atencion
from usuarios.models import Usuario

logger = logging.getLogger(__name__)

def enviar_notificacion_expediente(caso_id):
    caso = Caso_atencion.objects.get(id=caso_id)

    # Obtener ADMIN y COORD (reciben todas las notificaciones)
    admins_coords = Usuario.objects.filter(
        id_rol__clave__in=['ADMIN', 'COORD'],
        is_active=True,
    ).values_list('correo', flat=True)

    # Obtener el usuario asignado al caso (persona_consejera)
    destinatarios = list(admins_coords)
    
    if caso.persona_consejera and caso.persona_consejera.correo:
        # Agregar el correo de la persona consejera si no está ya en la lista
        if caso.persona_consejera.correo not in destinatarios:
            destinatarios.append(caso.persona_consejera.correo)

    if not destinatarios:
        logger.warning(f'No hay destinatarios para el expediente {caso.folio}')
        return f'No se envió correo para {caso.folio} - Sin destinatarios'

    asunto = f"Nuevo expediente creado: {caso.folio}"
    mensaje = f'''
    Se ha creado un nuevo expediente:
    
    Folio: {caso.folio}
    Tipo: {caso.tipo}
    Fecha: {caso.fecha_creacion}
    Estatus: {caso.estatus}
    Persona consejera: {caso.persona_consejera.get_full_name() if caso.persona_consejera else 'No asignada'}
    '''

    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        destinatarios,
        fail_silently=False,
    )

    logger.info(f'Notificación enviada para expediente {caso.folio} a {len(destinatarios)} destinatario(s)')
    return f'Correo enviado para {caso.folio} a {len(destinatarios)} destinatario(s)'

def log_envio_exitos(task):
    logger.info(f'Tarea completada: {task.result}')