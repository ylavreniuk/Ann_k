from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Calendar, Event, EventParticipant, CalendarShare, EventReminder, AvailabilitySlot

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Додаткова інформація', {'fields': ('phone', 'timezone', 'notification_email', 'notification_sms', 'avatar')}),
    )

@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'description', 'owner__username']
    date_hierarchy = 'created_at'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'calendar', 'start_time', 'end_time', 'status', 'created_by']
    list_filter = ['status', 'calendar', 'start_time']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_time'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'role', 'status', 'responded_at']
    list_filter = ['role', 'status']
    search_fields = ['event__title', 'user__username']

@admin.register(CalendarShare)
class CalendarShareAdmin(admin.ModelAdmin):
    list_display = ['calendar', 'user', 'permission', 'created_at']
    list_filter = ['permission', 'created_at']
    search_fields = ['calendar__name', 'user__username']

@admin.register(EventReminder)
class EventReminderAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'type', 'minutes_before', 'is_sent', 'sent_at']
    list_filter = ['type', 'is_sent']
    search_fields = ['event__title', 'user__username']

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ['user', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active']
    search_fields = ['user__username']