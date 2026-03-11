from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import async_task

from casos.models import Caso_atencion


@receiver(post_save, sender=Caso_atencion)
def notificar_nuevo_expediente(sender, instance, created, **kwargs):
    if created:
        async_task(
            'casos.tasks.enviar_notificacion_expediente',
            instance.id_caso,
            hook='casos.tasks.log_envio_exitoso'
        )