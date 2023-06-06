import requests
from time import sleep

import telegram
from environs import Env


def check_reviews(token, params=None):
    url = 'https://dvmn.org/api/long_polling/'
    try:
        response = requests.get(
            url, 
            headers = {
                'Authorization': f'Token {token}'
            },
            params=params
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        return None
    except requests.exceptions.ConnectionError:
        sleep(10)
        return None


def get_timestamp(new_reviews):
    if new_reviews.get('timestamp_to_request'):
        return new_reviews.get('timestamp_to_request')
    elif new_reviews.get('last_attempt_timestamp'):
        return new_reviews.get('last_attempt_timestamp')
    else:
        return None


def send_notifications(bot, new_reviews):
    attempts = new_reviews.get('new_attempts')
        for attempt in attempts:
            title = attempt.get('lesson_title')
            status = 'обнаружены ошибки' if attempt.get('is_negative') else 'работа принята'
            url = attempt.get('lesson_url')

            message = f'Урок "{title}" проверен, результат - {status}.\nСсылка на урок - {url}'
            bot.send_message(chat_id=chat_id, text=message)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    
    dvmn_token = env('DVMN_TOKEN')
    tg_api_token = env('TG_API_TOKEN')
    chat_id = env('CHAT_ID')
    
    bot = telegram.Bot(token=tg_api_token)
    
    params = {'timestamp': None}
    while True:
        new_reviews = check_reviews(dvmn_token, params)
        print(new_reviews)

        params['timestamp'] = get_timestamp(new_reviews)
        if new_reviews.get('status') == 'found':
            send_notifications(bot, new_reviews)
