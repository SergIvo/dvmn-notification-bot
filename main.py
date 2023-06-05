import requests

from environs import Env


def get_response(url, token):
    response = requests.get(
        url, 
        headers = {
            'Authorization': f'Token {token}'
        }
    )
    response.raise_for_status()
    return response.json()
    
    
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
        print(new_reviews)
