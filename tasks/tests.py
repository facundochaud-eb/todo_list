from django.test import TestCase
from .models import Priority
from .factories import TaskFactory, EventFactory, UserFactory
from parameterized import parameterized

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
