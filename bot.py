import requests
import telegram
import os
from time import sleep
from dotenv import load_dotenv


def main(bot_token, api_token, chat_id):
    bot = telegram.Bot(token=bot_token)
    headers = {
        'Authorization': f'Token {api_token}',
    }
    timestap = None
    while True:
        try:
            params = {
                'timestap': timestap
            }
            response = requests.get('https://dvmn.org/api/long_polling/',
                                    headers=headers, params=params)
            response_json = response.json()

            if response_json['status'] == 'timeout':
                timestap = response.json()['timestamp_to_request']
                continue

            lesson_title = response_json['new_attempts'][0]['lesson_title']
            lesson_url = response_json['new_attempts'][0]['lesson_url']
            if response_json['new_attempts'][0]['is_negative']:
                text = f'''У вас проверили работу "{lesson_title}"
{lesson_url}\n
К сожалению, в работе нашлись ошибки'''
            else:
                text = f'''У вас проверили работу "{lesson_title}"
{lesson_url}\n
Преподавателю всё понравилось, можно приступать к следущему уроку'''
            bot.send_message(chat_id=chat_id,
                             text=text)
        except requests.exceptions.ReadTimeout as e:
            print(f'{e}')
        except requests.exceptions.ConnectionError:
            print('connection error, reconnect...')
            sleep(5)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('TG_BOT_TOKEN')
    api_token = os.getenv('DEVMAN_API_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    main(token, chat_id)
