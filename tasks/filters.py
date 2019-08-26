import django_filters
from django import forms
from .models import Task, Priority, Event


class TaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Name'
    )
    priority = django_filters.ModelChoiceFilter(
        queryset=Priority.objects.all(),
        widget=forms.Select
    )
    event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(),
        widget=forms.Select
    )

    class Meta:
        model = Task
        fields = ['name', 'priority', 'event']
