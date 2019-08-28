from django.conf.urls import url
from . import views
# from .filters import TaskFilter
# from django_filters.views import FilterView


urlpatterns = [
    url(
        r'^(?P<pk_event>[0-9]+)/tasks/create',
        views.TaskCreate.as_view(),
        name='task_create'
    ),
    url(
        r'^(?P<pk_event>[0-9]+)/tasks/(?P<pk>[0-9]+)/update',
        views.TaskUpdate.as_view(),
        name='task_update'
    ),
    url(
        r'(?P<pk_event>[0-9]+)/tasks/(?P<pk>[0-9]+)/check',
        views.task_done,
        name='task_done'
    ),
    url(
        r'(?P<pk_event>[0-9]+)/tasks/(?P<pk>[0-9]+)/delete',
        views.TaskDelete.as_view(),
        name='task_delete'
    ),
    url(
        r'^(?P<pk_event>[0-9]+)/tasks',
        views.TasksList.as_view(),
        name="tasks_list"
    ),
    url(
        r'^$',
        views.EventsList.as_view(),
        name="events_list"
    ),
    # url(
    #     r'^$',
    #     views.TasksList.as_view(),
    #     FilterView.as_view(filterset_class=TaskFilter, template_name='tasks/task_filter.html'),
    #     name='task_list'
    # ),
]
