import requests
from time import sleep

from environs import Env


def get_response(url, token, params):
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
    
    
def check_reviews(token, params=None):
    url = 'https://dvmn.org/api/user_reviews/'
    reviews = get_response(url, token, params)
    return reviews


def make_long_poll(token, params=None):
    url = 'https://dvmn.org/api/long_polling/'
    reviews = get_response(url, token, params)
    return reviews


if __name__ == '__main__':
    env = Env()
    env.read_env()
    
    TOKEN = env('DVMN_TOKEN')
    params = {}
    while True:
        new_reviews = make_long_poll(TOKEN, params)
        print(new_reviews)
        if new_reviews.get('timestamp_to_request'):
            params['timestamp'] = new_reviews.get('timestamp_to_request')
        elif new_reviews.get('last_attempt_timestamp'):
            params['timestamp'] = new_reviews.get('last_attempt_timestamp')
