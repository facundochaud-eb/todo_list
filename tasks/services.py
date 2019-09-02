import requests
from tasks.models import Event

API_URL = 'https://www.eventbriteapi.com/v3/'

EVENTS = []


# TODO test
def get_event(user, event_id):
    # check "cache"
    for event in EVENTS:
        if event.id == event_id:
            return event
    # if not in cache
    token = get_token_from_user(user)
    url = API_URL + 'events/' + str(event_id)
    params = {'token': token}
    req = requests.get(url, params).json()
    event = Event(id=int(req['id']), name=req['name']['text'], user=user)
    EVENTS.append(event)
    print(f"API REQUEST: {event} DONE")
    return event


def get_events(user):
    url = API_URL + 'users/me/events/'
    params = {
        'token': get_token_from_user(user),
    }
    req = requests.get(url, params).json()['events']
    events = [
        Event(id=int(event['id']), name=event['name']['text'], user=user)
        for event in req
    ]
    print(f"API REQUEST: Events list")
    return events


def get_token_from_user(user):
    return user.social_auth.filter(provider='eventbrite')[0].access_token
