from django.dispatch import receiver
from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete


@receiver(cleanup_pre_delete, dispatch_uid="eahub.signals.sorl_delete")
def sorl_delete(sender, **kwargs):
    delete(kwargs["file"])
