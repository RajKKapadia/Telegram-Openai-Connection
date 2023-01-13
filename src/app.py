import os


from outside_apis.telegram_api import send_message, set_webhook, set_menu_commands
from helper.utils import process_request, generate_response


from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/telegram', methods=['POST'])
def telegram_api():

    if request.is_json:
        data = process_request(request)
        if data['secret_token'] == os.getenv('HEADER_TOKEN'):
            if data['is_text'] and not data['is_bot']:
                response = generate_response(data['message'])
                _ = send_message(data['sender_id'], response)
            elif data['is_bot']:
                response = 'I know you are a bot.'
                _ = send_message(data['sender_id'], response)
            else:
                pass    
            return 'OK', 200
        return 'OK', 200
    else:
        return 'OK', 200


@app.route('/set-telegram-webhook', methods=['POST'])
def set_telegram_webhook():

    if request.is_json:
        body = request.get_json()
        flag = set_webhook(body['url'], body['secret_token'])
        if flag:
            return 'OK', 200
        else:
            return 'BAD REQUEST', 400
    else:
        return 'BAD REQUEST', 400


@app.route('/set-telegram-menu-commands', methods=['POST'])
def set_telegram_menu_commands():

    if request.is_json:
        body = request.get_json()
        flag = set_menu_commands(body['commands'])
        if flag:
            return 'OK', 200
        else:
            return 'BAD REQUEST', 400
    else:
        return 'BAD REQUEST', 400