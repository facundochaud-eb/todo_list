import requests
from tasks.models import Event

API_URL = 'https://www.eventbriteapi.com/v3/'


def get_user(token):
    url = API_URL + 'users/me/'
    params = {
        'token': token,
    }
    return requests.get(url, params).json()


def get_event(user, event_id):
    token = get_token_from_user(user)
    url = API_URL + 'events/' + str(event_id)
    params = {
        'token': token,
    }
    req = requests.get(url, params).json()
    return Event(id=req['id'], name=req['name']['text'], user=user)


def get_events(token, user):
    url = API_URL + 'users/me/events/'
    params = {
        'token': token,
    }
    req = requests.get(url, params).json()['events']
    events = [
        Event(id=event['id'], name=event['name']['text'], user=user)
        for event in req
    ]
    return events


def get_token(request):
    return request.user.social_auth.filter(provider='eventbrite')[0].access_token


def get_token_from_user(user):
    return user.social_auth.filter(provider='eventbrite')[0].access_token
