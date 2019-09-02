import factory
from django.conf import settings
from .models import Priority, Task, Event
import random


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: f'user_{n}')
    password = factory.Faker('password')


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Sequence(lambda n: f'Event_{n}')
    user = factory.SubFactory(UserFactory)


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Sequence(lambda n: f'Task_{n}')
    done = False
    priority = factory.Iterator(Priority.objects.all())
    user = factory.SubFactory(UserFactory)
    event_id = random.randint(0, 10**11)
