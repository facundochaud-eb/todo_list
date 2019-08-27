from django.conf.urls import url
from . import views
from .filters import TaskFilter
from django_filters.views import FilterView


urlpatterns = [
    # url(r'^$', views.TasksList.as_view(), name='task_list'),
    url(
        r'^$',
        FilterView.as_view(filterset_class=TaskFilter, template_name='tasks/task_filter.html'),
        name='task_list'
    ),
    url(
        r'^create',
        views.TaskCreate.as_view(),
        name='task_create'
    ),
    url(
        r'(?P<pk>[0-9]+)/update',
        views.TaskUpdate.as_view(),
        name='task_update'
    ),
    url(
        r'(?P<pk>[0-9]+)/check',
        views.task_done,
        name='task_done'
    ),
]
