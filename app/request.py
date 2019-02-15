import urllib.request, json
from .models import *

# getting api key

base_url = None

# getting the news base url


def configure_request(app):
    base_url = app.config['QUOTES_API_BASE_URL']


