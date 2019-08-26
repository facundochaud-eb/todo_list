from django.contrib import admin
from .models import (
    Priority, Event, Task
)

# Register your models here.
admin.site.register(Event)
admin.site.register(Priority)
admin.site.register(Task)
