from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    notification_email = models.BooleanField(default=True)
    notification_sms = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
class Calendar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendars')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3B82F6')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']

class Event(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Заплановано'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=300, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    all_day = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    color = models.CharField(max_length=7, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
        
class EventParticipant(models.Model):
    ROLE_CHOICES = [
        ('organizer', 'Організатор'),
        ('required', 'Обов\'язковий'),
        ('optional', 'Необов\'язковий'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Очікується'),
        ('accepted', 'Прийнято'),
        ('declined', 'Відхилено'),
        ('tentative', 'Можливо'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participations')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='required')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['event', 'user']

class CalendarShare(models.Model):
    PERMISSION_CHOICES = [
        ('view', 'Перегляд'),
        ('edit', 'Редагування'),
        ('admin', 'Адміністрування'),
    ]
    
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_calendars')
    permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES, default='view')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['calendar', 'user']

class EventReminder(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push-повідомлення'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='email')
    minutes_before = models.IntegerField(default=30)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
class AvailabilitySlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability_slots')
    day_of_week = models.IntegerField(choices=[(i, i) for i in range(7)])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']