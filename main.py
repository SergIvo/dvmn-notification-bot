import requests
from time import sleep

import telegram
from environs import Env


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


if __name__ == '__main__':
    env = Env()
    env.read_env()

    dvmn_token = env('DVMN_TOKEN')
    tg_api_token = env('TG_API_TOKEN')
    chat_id = env('TG_CHAT_ID')

    bot = telegram.Bot(token=tg_api_token)

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
