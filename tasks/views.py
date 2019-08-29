from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Task, Event
from . import services


class EventsList(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'tasks/events_list.html'

    def get_queryset(self):
        token = services.get_token(self.request)
        return services.get_events(token, self.request.user)


class TasksList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks_list.html"

    def get_queryset(self):
        event_id = self.kwargs['pk_event']
        return Task.objects.filter(event_id=event_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = services.get_event(self.request.user, self.kwargs['pk_event'])
        context['event'] = event
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'done', 'priority']

    def get_success_url(self):
        return reverse_lazy('tasks_list', kwargs=self.kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.event_id = self.kwargs['pk_event']
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = services.get_event(self.request.user, self.kwargs['pk_event'])
        context['event'] = event
        return context


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'done', 'priority']

    def get_success_url(self):
        return reverse_lazy(
            'tasks_list',
            kwargs={'pk_event': self.kwargs['pk_event']}
        )

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.event_id = self.kwargs['pk_event']
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = services.get_event(self.request.user, self.kwargs['pk_event'])
        context['event'] = event
        return context


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task

    def get_success_url(self):
        return reverse_lazy(
            'tasks_list',
            kwargs={'pk_event': self.kwargs['pk_event']}
        )


def task_done(request, pk_event, pk):
    task = Task.objects.get(pk=pk)
    task.done = not task.done
    task.save()
    return redirect('tasks_list', pk_event=pk_event)


class Login(LoginView):
    template_name = 'login.html'


class Logout(LogoutView):
    template_name = ''
