import logging
from os import getenv
from time import sleep

from dotenv import load_dotenv
import telegram
import requests


def main():
    load_dotenv()
    telegram_token = getenv('TELEGRAM_TOKEN')
    devman_token = getenv('DEVMAN_TOKEN')
    telegram_chat_id = getenv('TELEGRAM_CHAT_ID')

    header = {'Authorization': devman_token}
    url = 'https://dvmn.org/api/long_polling/'
    timestamp = None

    bot = telegram.Bot(token=telegram_token)

    logging.warning('Бот запущен')

    while True:
        try:
            response = requests.get(
                url,
                headers=header,
                params={'timestamp': timestamp}
            )
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
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


if __name__ == "__main__":
    main()
