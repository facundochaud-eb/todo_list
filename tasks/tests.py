from django.test import TestCase
import json
from parameterized import parameterized
from unittest.mock import patch
from social_django.models import UserSocialAuth

from . import services
from .models import Priority, Event
from .factories import TaskFactory, EventFactory, UserFactory
from todolistsite import get_env_variable

PRIORITIES = ["LOW", "NORMAL", "URGENT"]


def mocked_requests_get_events(*args, **_):
    class MockResponse:
        def __init__(self, json_data=None, status_code=200):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            with open('tasks/tests/api_response_events.json', 'r') as f:
                return json.loads(f.read())

        def raise_for_status(self):
            pass
    return MockResponse()


def mocked_requests_get_event(*args, **_):
    class MockResponse:
        def __init__(self, json_data=None, status_code=200):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            with open('tasks/tests/api_response_event.json', 'r') as f:
                return json.loads(f.read())

        def raise_for_status(self):
            pass
    return MockResponse()


class TaskServicesTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.user_social = UserSocialAuth.objects.create(
            user=self.user,
            provider='eventbrite',
            extra_data={
                'auth_time': 1567438201,
                'access_token': get_env_variable('ACCESS_TOKEN'),
                'token_type': 'bearer'
            }
        )

    def test_get_token_from_user(self):
        self.assertEqual(services.get_token_from_user(self.user), get_env_variable('ACCESS_TOKEN'))

    @patch('tasks.services.requests.get', return_value=mocked_requests_get_events())
    def test_get_events(self, mocked_request):
        events = services.get_events(self.user)
        self.assertEqual(mocked_request.call_args[0][0], 'https://www.eventbriteapi.com/v3/users/me/events/')
        self.assertEqual(mocked_request.call_args[0][1]['token'], get_env_variable('ACCESS_TOKEN'))
        self.assertEqual(18, len(events))
        for event in events:
            self.assertIsInstance(event, Event)
            self.assertEqual(event.user, self.user)

    @patch('tasks.services.requests.get', return_value=mocked_requests_get_event())
    def test_get_event_one_time(self, mocked_request):
        event_expected = Event(
            id=68265236159,
            name='PASO Nacional 2019',
            user=self.user
        )
        event_result = services.get_event(self.user, 68265236159)
        self.assertIsInstance(event_result, Event)
        self.assertEqual(event_result.id, event_expected.id)
        self.assertEqual(event_result.name, event_expected.name)
        self.assertEqual(event_result.user, event_expected.user)

    # test two, three times for cache


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
        priority = Priority(name=name)
        self.assertEqual(str(priority), name)

    def test_event_str(self):
        event = EventFactory.build()
        self.assertIn(str(event.id),   str(event))
        self.assertIn(str(event.name), str(event))
        self.assertIn(str(event.user), str(event))

    def test_task_str(self):
        event = EventFactory.build()
        services.EVENTS.append(event)
        task = TaskFactory.build(
            user=event.user,
            event_id=event.id
        )
        self.assertIn(str(task.name),     str(task))
        self.assertIn(str(task.done),     str(task))
        self.assertIn(str(task.priority), str(task))
        self.assertIn(str(task.event),    str(task))
