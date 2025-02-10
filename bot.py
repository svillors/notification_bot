import requests
import telegram
import os
from time import sleep
from dotenv import load_dotenv


def main():
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    api_token = os.environ['DEVMAN_API_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
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
            response = response.json()

            if response['status'] == 'timeout':
                timestap = response.json()['timestamp_to_request']
                continue

            lesson_title = response['new_attempts'][0]['lesson_title']
            lesson_url = response['new_attempts'][0]['lesson_url']
            if response['new_attempts'][0]['is_negative']:
                text = f'''У вас проверили работу "{lesson_title}"
{lesson_url}\n
К сожалению, в работе нашлись ошибки'''
            else:
                text = f'''У вас проверили работу "{lesson_title}"
{lesson_url}\n
Преподавателю всё понравилось, можно приступать к следущему уроку'''
            bot.send_message(chat_id=chat_id,
                             text=text)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('connection error, reconnect...')
            sleep(5)


if __name__ == "__main__":
    main()
