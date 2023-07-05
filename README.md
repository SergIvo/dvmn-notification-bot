# Devman Notification Bot

## About

This application is a simple Telegram bot what fetches data about newly reviewed works from Devman API, extracts and formats the information and sends it to a certain Telegram channel.

This application created for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/)

## Running the application

1. Download files from GitHub with `git clone` command:
```
git clone https://github.com/SergIvo/dvmn-notification-bot
```
2. Create virtual environment using python [venv](https://docs.python.org/3/library/venv.html) to avoid conflicts with different versions of the same packages:
```
python -m venv venv
```
3. Then install dependencies from "requirements.txt" in created virtual environment using `pip` package manager:
```
pip install -r requirements.txt
```
4. To run the application, you should first set these environment variables:
```
export DVMN_TOKEN="your Devman API key"
export TG_API_KEY="your Telegram API key"
export TG_CHAT_ID="id of your Telegram chat with your bot"
```

To make environment variable management easier, you can create [.env](https://pypi.org/project/python-dotenv/#getting-started) file and store all variables in it. 

5. Then simply run `main.py`:
```
python main.py
```
Bot will constantly make requests to Devman API and send notifications to Telegram chat if any new reviews will occure.

## Running application in Docker container

To run application in Docker, you should first create Docker image with this application by following command:
```
docker build -t notification_bot .
```

This will create image with name `notification_bot` and tag `latest`. You can see it in the list of Docker images by executing command `docker images`

For convinience, list all your environment variables in the [.env](https://pypi.org/project/python-dotenv/#getting-started) file, in `KEY=VALUE` format, like this:
```
DVMN_TOKEN=your_Devman_API_key
TG_API_KEY=your_Telegram_API_key
TG_CHAT_ID=id_of_your_Telegram_chat_with_your_bot
```
After that, execute the following command to create Docker container with name `notification_bot`:
```
docker run --name notification_bot --env-file ./.env -d notification_bot:latest
```

Now you can find your container in the list of existing containers by executing command `docker ps -a`
