from .base import *
from settings import get_env_variable


SOCIAL_AUTH_EVENTBRITE_KEY = get_env_variable('SOCIAL_AUTH_EVENTBRITE_KEY')
SOCIAL_AUTH_EVENTBRITE_SECRET = get_env_variable('SOCIAL_AUTH_EVENTBRITE_SECRET')
