from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Calendar, Event, EventParticipant, EventReminder
from .forms import EventForm, CalendarForm
import json

@login_required
def dashboard(request):
    user_calendars = Calendar.objects.filter(
        Q(owner=request.user) | Q(shares__user=request.user)
    ).distinct()
    
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(
        calendar__in=user_calendars,
        start_time__gte=today,
        status__in=['scheduled', 'confirmed']
    ).select_related('calendar', 'created_by')[:10]
    
    context = {
        'calendars': user_calendars,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'booking/dashboard.html', context)

@login_required
def calendar_view(request, calendar_id=None):
    if calendar_id:
        calendar = get_object_or_404(Calendar, id=calendar_id)
        if not (calendar.owner == request.user or 
                calendar.shares.filter(user=request.user).exists() or 
                calendar.is_public):
            return HttpResponse("Доступ заборонено", status=403)
    else:
        calendar = None
    
    user_calendars = Calendar.objects.filter(
        Q(owner=request.user) | Q(shares__user=request.user)
    ).distinct()
    
    context = {
        'calendar': calendar,
        'user_calendars': user_calendars,
    }
    return render(request, 'booking/calendar.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            form.save_m2m()
            
            # Створити нагадування
            if form.cleaned_data.get('reminder_minutes'):
                EventReminder.objects.create(
                    event=event,
                    user=request.user,
                    minutes_before=form.cleaned_data['reminder_minutes']
                )
            
            if request.headers.get('HX-Request'):
                return render(request, 'booking/partials/event_card.html', {'event': event})
            
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(user=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'booking/event_form.html', context)

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    can_view = (
        event.calendar.owner == request.user or
        event.calendar.shares.filter(user=request.user).exists() or
        event.participants.filter(user=request.user).exists() or
        event.calendar.is_public
    )
    
    if not can_view:
        return HttpResponse("Доступ заборонено", status=403)
    
    can_edit = (
        event.calendar.owner == request.user or
        event.calendar.shares.filter(
            user=request.user, 
            permission__in=['edit', 'admin']
        ).exists() or
        event.created_by == request.user
    )
    
    context = {
        'event': event,
        'can_edit': can_edit,
        'user_participation': event.participants.filter(user=request.user).first()
    }
    return render(request, 'booking/event_detail.html', context)

@login_required
@require_http_methods(["POST"])
def respond_to_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participation = get_object_or_404(EventParticipant, event=event, user=request.user)
    
    status = request.POST.get('status')
    if status in ['accepted', 'declined', 'tentative']:
        participation.status = status
        participation.responded_at = timezone.now()
        participation.save()
    
    if request.headers.get('HX-Request'):
        return render(request, 'booking/partials/event_response.html', {
            'participation': participation
        })
    
    return redirect('event_detail', event_id=event.id)

@login_required
def api_events(request):
    """API endpoint для FullCalendar.js"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    calendar_ids = request.GET.getlist('calendars[]')
    
    events_query = Event.objects.filter(
        Q(calendar__owner=request.user) |
        Q(calendar__shares__user=request.user) |
        Q(participants__user=request.user)
    ).distinct()
    
    if calendar_ids:
        events_query = events_query.filter(calendar_id__in=calendar_ids)
    
    if start and end:
        events_query = events_query.filter(
            start_time__lte=end,
            end_time__gte=start
        )
    
    events = []
    for event in events_query:
        events.append({
            'id': str(event.id),
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'allDay': event.all_day,
            'color': event.color or event.calendar.color,
            'url': f'/events/{event.id}/',
            'extendedProps': {
                'description': event.description,
                'location': event.location,
                'status': event.status,
                'calendar': event.calendar.name,
            }
        })
    
    return JsonResponse(events, safe=False)

@login_required
@require_http_methods(["GET", "POST"])
def create_calendar(request):
    if request.method == "POST":
        form = CalendarForm(request.POST)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.owner = request.user
            calendar.save()
            
            if request.headers.get('HX-Request'):
                return HttpResponse(
                    status=204,
                    headers={'HX-Redirect': f'/calendar/{calendar.id}/'}
                )
            
            return redirect('calendar_detail', calendar_id=calendar.id)
    else:
        form = CalendarForm()
    
    context = {
        'form': form,
    }
    return render(request, 'booking/calendar_form.html', context)

# Статистика для dashboard
@login_required
def stats_week_events(request):
    start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
    end_of_week = start_of_week + timedelta(days=7)
    
    count = Event.objects.filter(
        Q(calendar__owner=request.user) | Q(participants__user=request.user),
        start_time__date__gte=start_of_week,
        start_time__date__lt=end_of_week,
        status__in=['scheduled', 'confirmed']
    ).distinct().count()
    
    return HttpResponse(str(count))

@login_required
def stats_pending_responses(request):
    count = EventParticipant.objects.filter(
        user=request.user,
        status='pending',
        event__start_time__gte=timezone.now()
    ).count()
    
    return HttpResponse(str(count))

@login_required
def stats_hours_planned(request):
    events = Event.objects.filter(
        Q(calendar__owner=request.user) | Q(participants__user=request.user),
        start_time__gte=timezone.now(),
        status__in=['scheduled', 'confirmed']
    ).distinct()
    
    total_hours = sum(
        (event.end_time - event.start_time).total_seconds() / 3600
        for event in events
    )
    
    return HttpResponse(f"{int(total_hours)}")