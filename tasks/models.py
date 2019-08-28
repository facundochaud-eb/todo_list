from django.conf import settings
from django.db import models


class Priority(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    done = models.BooleanField()
    priority = models.ForeignKey(
        'Priority',
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"<Task: {self.name}, done? {self.done}, priority: {self.priority}, event: {self.event}>"


class Event(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"<Event: {self.name} from {self.user}>"
