
import json

import yaml
from loguru import logger
import requests
from flask import Flask, request

app = Flask(__name__)

### Load config
config = yaml.safe_load(
    open('config.yml')
)
key = config.get('key')
token = key.get('token')

web = config.get('web')
HOST = web.get('host')
PORT = web.get('port')


### default header
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def post_message(text:str, senderId:str ,headers=headers, token=token):

    url = f'https://us-central1-hahamut-8888.cloudfunctions.net/messagePush?access_token={token}'

    data = {
        'recipient':{
            'id': senderId
        },
        'message':{
            'type': 'text',
            'text': text
        }
    }

    requests.post(url=url, json=data, headers=headers)


@app.route('/', methods=['POST', 'GET'])
def response():
    if request.method == 'POST':
        """
        Receive POST format
        {
            'botid': 'bot@<ID>',
            'time': 1616654861527,
            'messaging': [
                {
                    'sender_id': 'sender_id',
                    'message': {
                        'text': '123'
                    }
                }
            ]
        }
        """

        requestJson = json.loads(request.data)
        logger.info(requestJson)

        _ = requestJson.get('time')
        text = requestJson.get('messaging')[0].get('message').get('text')
        senderId = requestJson.get('messaging')[0].get('sender_id')

        post_message(text, senderId)

        return 'YEE', 200
    else:
        return 'Noooooo', 500


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)