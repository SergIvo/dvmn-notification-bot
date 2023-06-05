import requests
from time import sleep

from environs import Env


def get_response(url, token):
    try:
        response = requests.get(
            url, 
            headers = {
                'Authorization': f'Token {token}'
            },
            timeout = 10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        return None
    except requests.exceptions.ConnectionError:
        sleep(10)
        return None
    
    
def check_reviews(token):
    url = 'https://dvmn.org/api/user_reviews/'
    reviews = get_response(url, token)
    return reviews


def make_long_poll(token):
    url = 'https://dvmn.org/api/long_polling/'
    reviews = get_response(url, token)
    return reviews


if __name__ == '__main__':
    env = Env()
    env.read_env()
    
    TOKEN = env('DVMN_TOKEN')
    while True:
        new_reviews = make_long_poll(TOKEN)
        if new_reviews:
            print(new_reviews)
