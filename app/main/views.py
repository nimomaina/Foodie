from flask import Flask, render_template
from . import main
import requests
import json


@main.route("/")
def index():
    r = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    quote = r['quote']
    return render_template('index.html', quote=quote)

