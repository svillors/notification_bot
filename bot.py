import requests
import telegram
import os
import logging
from time import sleep
from dotenv import load_dotenv


load_dotenv()
API_TOKEN = os.environ['DEVMAN_API_TOKEN']
CHAT_ID = os.environ['TG_CHAT_ID']
BOT = telegram.Bot(token=os.environ['TG_BOT_TOKEN'])


class TelegramBotHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        if record.exc_info:
            traceback = self.formatException(record.exc_info)
            message = f"Бот упал с ошибкой:\n\n{traceback}"
        else:
            message = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=message)


logger = logging.getLogger('tg_bot_logger')
logger.setLevel(logging.INFO)
logger.addHandler(TelegramBotHandler(BOT, CHAT_ID))


def main():
    logger.info("Бот запущен!")
    headers = {
        'Authorization': f'Token {API_TOKEN}',
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
            BOT.send_message(chat_id=CHAT_ID,
                             text=text)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            logger.error('connection error, reconnect...')
            sleep(10)
        except Exception:
            logger.exception()


if __name__ == "__main__":
    main()
