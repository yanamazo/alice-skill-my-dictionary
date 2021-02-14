from __future__ import unicode_literals
import json
import logging
from sheety import SheetyManager
import requests
from flask import Flask, request

application = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
sessionStorage = {}

DICT_API_KEY = 'dict.1.1.2021...'
DICT_URL = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
GOOGLE_SHEET = 'https://api.sheety.co/.../myWords/words'
PASSWORD = '...'

@application.route("/", methods=['POST'])

def main(request):
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    # logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Какое слово перевести?'
        return

    word = req['request']['original_utterance']
    params = {
        'key': DICT_API_KEY,
        'lang': 'ru-en',
        'text': word
    }
    response = requests.get(url=DICT_URL, params=params).json()
    translated_word = response['def'][0]['tr'][0]['text']
    res['response']['text'] = translated_word
    my_google_dict = SheetyManager(
        url=GOOGLE_SHEET,
        auth_method='bearer',
        token=PASSWORD)
    my_google_dict.add_data(rus=word, eng=translated_word)
    return
