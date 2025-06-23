from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventParticipant
from .tasks import send_event_invitation

@receiver(post_save, sender=EventParticipant)
def notify_participant(sender, instance, created, **kwargs):
    if created and instance.role != 'organizer':
        # Відправити запрошення асинхронно
        send_event_invitation.delay(instance.event.id, instance.user.id)