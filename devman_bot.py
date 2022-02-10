from os import getenv
from pprint import pprint

from dotenv import load_dotenv
import telegram
import requests


def send_message(token, chat_id, lesson_title, result, lesson_url):
    bot = telegram.Bot(token=token)
    text = 'Преподаватель проверил работу "{}"! {}. {}'.format(
        lesson_title, result, lesson_url
    )
    bot.send_message(
        chat_id=chat_id,
        text=text)


def main():
    load_dotenv()
    telegram_token = getenv('TELEGRAM_TOKEN')
    devman_token = getenv('DEVMAN_TOKEN')
    telegram_chat_id = getenv('TELEGRAM_CHAT_ID')

    header = {'Authorization': devman_token}
    url = 'https://dvmn.org/api/long_polling/'
    timestamp = None

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
            continue

        server_message = response.json()
        timestamp = server_message.get('timestamp_to_request')

        if server_message['status'] == 'found':
            attempts = server_message['new_attempts']

            for attempt in attempts:
                lesson_title = attempt['lesson_title']
                lesson_url = attempt['lesson_url']
                if attempt['is_negative']:
                    result = 'Работа не принята'
                else:
                    result = 'Работа принята'
                pprint(attempt)
                send_message(
                    telegram_token, telegram_chat_id,
                    lesson_title, result, lesson_url
                )


if __name__ == "__main__":
    main()
