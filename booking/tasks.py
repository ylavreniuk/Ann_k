from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import timedelta
from .models import EventReminder, Event, EventParticipant
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_event_reminders():
    """Відправка нагадувань про події"""
    now = timezone.now()
    
    reminders = EventReminder.objects.filter(
        is_sent=False,
        event__status__in=['scheduled', 'confirmed'],
        event__start_time__gt=now
    ).select_related('event', 'user', 'event__calendar')
    
    sent_count = 0
    for reminder in reminders:
        reminder_time = reminder.event.start_time - timedelta(minutes=reminder.minutes_before)
        
        if now >= reminder_time:
            try:
                if reminder.type == 'email' and reminder.user.notification_email:
                    send_email_reminder.delay(reminder.id)
                    sent_count += 1
                
                reminder.is_sent = True
                reminder.sent_at = now
                reminder.save()
                
            except Exception as e:
                logger.error(f"Error sending reminder {reminder.id}: {str(e)}")
    
    return f"Processed {sent_count} reminders"

@shared_task
def send_email_reminder(reminder_id):
    """Відправка email нагадування"""
    try:
        reminder = EventReminder.objects.select_related(
            'event', 'user', 'event__calendar'
        ).get(id=reminder_id)
        
        subject = f"Нагадування: {reminder.event.title}"
        
        context = {
            'user': reminder.user,
            'event': reminder.event,
            'calendar': reminder.event.calendar,
            'minutes_before': reminder.minutes_before,
        }
        
        html_message = render_to_string('booking/emails/event_reminder.html', context)
        plain_message = render_to_string('booking/emails/event_reminder.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email='noreply@booking-system.com',
            recipient_list=[reminder.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Email reminder sent to {reminder.user.email} for event {reminder.event.id}")
        
    except Exception as e:
        logger.error(f"Failed to send email reminder {reminder_id}: {str(e)}")
        raise

@shared_task
def send_event_invitation(event_id, participant_id):
    """Відправка запрошення на подію"""
    try:
        participant = EventParticipant.objects.select_related(
            'event', 'user', 'event__created_by'
        ).get(event_id=event_id, user_id=participant_id)
        
        subject = f"Запрошення: {participant.event.title}"
        
        context = {
            'participant': participant,
            'event': participant.event,
            'organizer': participant.event.created_by,
        }
        
        html_message = render_to_string('booking/emails/event_invitation.html', context)
        plain_message = render_to_string('booking/emails/event_invitation.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email='noreply@booking-system.com',
            recipient_list=[participant.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Invitation sent to {participant.user.email} for event {event_id}")
        
    except Exception as e:
        logger.error(f"Failed to send invitation: {str(e)}")
        raise

@shared_task
def cleanup_old_events():
    """Видалення старих подій"""
    cutoff_date = timezone.now() - timedelta(days=365)
    
    old_events = Event.objects.filter(
        end_time__lt=cutoff_date,
        status='completed'
    )
    
    count = old_events.count()
    old_events.delete()
    
    logger.info(f"Deleted {count} old events")
    return f"Deleted {count} old events"