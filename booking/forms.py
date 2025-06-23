from django import forms
from django.db.models import Q
from .models import Event, Calendar, EventParticipant, User

class EventForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '5'
        })
    )
    
    reminder_minutes = forms.ChoiceField(
        choices=[
            ('', 'Без нагадування'),
            ('15', 'За 15 хвилин'),
            ('30', 'За 30 хвилин'),
            ('60', 'За 1 годину'),
            ('1440', 'За 1 день'),
        ],
        required=False
    )
    
    class Meta:
        model = Event
        fields = ['calendar', 'title', 'description', 'location', 
                  'start_time', 'end_time', 'all_day', 'color']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Тільки календарі з правами на редагування
            self.fields['calendar'].queryset = Calendar.objects.filter(
                Q(owner=user) | 
                Q(shares__user=user, shares__permission__in=['edit', 'admin'])
            ).distinct()
            
            # Всі користувачі крім поточного
            self.fields['participants'].queryset = User.objects.exclude(id=user.id)
    
    def save(self, commit=True):
        event = super().save(commit=commit)
        
        if commit:
            # Додати учасників
            participants = self.cleaned_data.get('participants', [])
            for user in participants:
                EventParticipant.objects.create(
                    event=event,
                    user=user,
                    role='required'
                )
            
            # Додати організатора
            EventParticipant.objects.create(
                event=event,
                user=event.created_by,
                role='organizer',
                status='accepted'
            )
        
        return event

class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['name', 'description', 'color', 'is_public']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }