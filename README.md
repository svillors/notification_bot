# Bot for notifications

## Description
This bot is designed for receiving notifications from the [Devman](https://dvmn.org/) API

## Environment
### Requirements
you should install all dependencies using:
```
$ pip install -r requirements.txt
```
### Environment variables
first you should add some values ​​in .env file:
- TG_BOT_TOKEN - telegram bot's token
- DEVMAN_API_TOKEN - API token for Devman
- TG_CHAT_ID - your telegram id
#### How to get
bot token: to get it you should create your own bot using [BotFather](https://telegram.me/BotFather)
Devmam API token: You need to be a student at Devman to obtain this token in the [Devman Api](https://dvmn.org/api/docs/)
telegram id: You can get your telegram ID using [UserInfoBot](https://telegram.me/userinfobot)
## Run
to run script you should use:
```
$ python3 bot.py
```
