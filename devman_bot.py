import logging
from os import getenv
from time import sleep

from dotenv import load_dotenv
import telegram
import requests


class MyLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    telegram_token = getenv('TELEGRAM_TOKEN')
    devman_token = getenv('DEVMAN_TOKEN')
    telegram_chat_id = getenv('TELEGRAM_CHAT_ID')

    header = {'Authorization': devman_token}
    url = 'https://dvmn.org/api/long_polling/'
    timestamp = None

    bot = telegram.Bot(token=telegram_token)

    logger = logging.getLogger("Телеграм-логер")
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler(bot, telegram_chat_id))

    logger.info('Бот запущен')

    while True:
        try:
            try:
                response = requests.get(
                    url,
                    headers=header,
                    params={'timestamp': timestamp},
                )
                response.raise_for_status()
            except requests.exceptions.ReadTimeout:
                logger.warning('Истекло время ожидания ответа от сервера')
                continue
            except requests.exceptions.ConnectionError:
                logger.warning('Потеряно соединение')
                sleep(60)
                continue

            server_message = response.json()

            if server_message['status'] == 'found':
                timestamp = server_message.get('last_attempt_timestamp')
                attempts = server_message['new_attempts']

                for attempt in attempts:
                    lesson_title = attempt['lesson_title']
                    lesson_url = attempt['lesson_url']
                    if attempt['is_negative']:
                        result = 'Работа не принята'
                    else:
                        result = 'Работа принята'

                    text = 'Преподаватель проверил работу "{}"! {}. {}'.format(
                        lesson_title, result, lesson_url
                    )
                    bot.send_message(
                        chat_id=telegram_chat_id,
                        text=text)

            elif server_message['status'] == 'timeout':
                timestamp = server_message.get('timestamp_to_request')

        except Exception as err:
            msg = f'Бот упал с ошибкой {err}.'
            logger.exception(msg)
            sleep(60)

if __name__ == "__main__":
    main()
