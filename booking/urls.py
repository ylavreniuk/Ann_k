from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/<uuid:calendar_id>/', views.calendar_view, name='calendar_detail'),
    path('calendar/create/', views.create_calendar, name='create_calendar'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<uuid:event_id>/', views.event_detail, name='event_detail'),
    path('events/<uuid:event_id>/respond/', views.respond_to_event, name='respond_to_event'),
    path('api/events/', views.api_events, name='api_events'),
    
    # HTMX endpoints for stats
    path('htmx/stats/week-events/', views.stats_week_events, name='stats_week_events'),
    path('htmx/stats/pending-responses/', views.stats_pending_responses, name='stats_pending_responses'),
    path('htmx/stats/hours-planned/', views.stats_hours_planned, name='stats_hours_planned'),
]