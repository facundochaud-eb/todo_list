from django.views.generic.list import ListView
from django.views.generic import (
    CreateView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Task


class TasksList(ListView):
    model = Task


class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task_list')


class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task_list')


def task_done(request, pk):
    task = Task.objects.get(pk=pk)
    task.done = not task.done
    task.save()
    return redirect('task_list')
