import logging
from time import sleep

import requests
import telegram
from environs import Env


class TgLogsHandler(logging.Handler):
    def __init__(self, tg_api_token, tg_chat_id):
        super().__init__()
        self.bot = telegram.Bot(token=tg_api_token)
        self.chat_id = tg_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(
            chat_id=self.chat_id,
            text=log_entry
        )


def fetch_reviews_from_api(token, params=None):
    url = 'https://dvmn.org/api/long_polling/'
    response = requests.get(
        url,
        headers={
            'Authorization': f'Token {token}'
        },
        params=params
    )
    response.raise_for_status()
    return response.json()


def send_notifications(bot, new_reviews):
    attempts = new_reviews.get('new_attempts')
    for attempt in attempts:
        title = attempt.get('lesson_title')
        if attempt.get('is_negative'):
            status = 'В работе обнаружены ошибки'
        else:
            status = 'Работа принята'
        url = attempt.get('lesson_url')

        message = f'Урок "{title}" проверен. {status}.\nСсылка на урок - {url}'
        bot.send_message(chat_id=chat_id, text=message)


def run_bot_main_loop(bot, dvmn_token):
    params = {'timestamp': None}
    while True:
        try:
            new_reviews = fetch_reviews_from_api(dvmn_token, params)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            sleep(10)
            continue

        if not new_reviews:
            continue

        if new_reviews.get('timestamp_to_request'):
            params['timestamp'] = new_reviews.get('timestamp_to_request')
        elif new_reviews.get('last_attempt_timestamp'):
            params['timestamp'] = new_reviews.get('last_attempt_timestamp')

        if new_reviews.get('status') == 'found':
            send_notifications(bot, new_reviews)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    dvmn_token = env('DVMN_TOKEN')
    tg_api_token = env('TG_API_TOKEN')
    chat_id = env('TG_CHAT_ID')

    bot = telegram.Bot(token=tg_api_token)

    handler = TgLogsHandler(tg_api_token, chat_id)
    handler.setFormatter(
        logging.Formatter('%(process)d %(levelname)s %(message)s')
    )

    logger = logging.getLogger('notification-bot')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.info('Bot started')

    while True:
        try:
            run_bot_main_loop(bot, dvmn_token)
        except Exception as ex:
            logger.exception(ex)
