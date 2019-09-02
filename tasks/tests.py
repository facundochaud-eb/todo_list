from django.test import TestCase, Client
from .models import Priority
from .factories import TaskFactory, EventFactory, UserFactory
from parameterized import parameterized
from . import services

PRIORITIES = ["LOW", "NORMAL", "URGENT"]


# Create your tests here.
class TaskModelsTestCase(TestCase):
    def setUp(self):
        # Priorities
        Priority.objects.create(name="LOW")
        Priority.objects.create(name="NORMAL")
        Priority.objects.create(name="URGENT")

    @parameterized.expand([
        ("LOW",),
        ("NORMAL",),
        ("URGENT",),
    ])
    def test_priority_str(self, name):
        priority = Priority.objects.create(name=name)
        self.assertEqual(str(priority), name)

    def test_event_str(self):
        event = EventFactory.create()
        self.assertIn(str(event.id),   str(event))
        self.assertIn(str(event.name), str(event))
        self.assertIn(str(event.user), str(event))

    def test_task_str(self):
        event = EventFactory.create()
        services.EVENTS.append(event)
        task = TaskFactory.create(
            user=event.user,
            event_id=event.id
        )
        self.assertIn(str(task.name),     str(task))
        self.assertIn(str(task.done),     str(task))
        self.assertIn(str(task.priority), str(task))
        self.assertIn(str(task.event),    str(task))


class TaskServicesTestCase(TestCase):
    def setUp(self):
        pass
