# PriceTracker
Simple script to parse prices on virtually any site you want.

This project needs to be self-hosted and requires some basic technical skills on:
- Bots for Telegram
- Parsing XPATH values from a website

This script allows you to set a desired price for a certain product and receive an alert whenever the actual price is lower or equal than the desired price. The alert will be sent on Telegram.

# Requirements
- Python3
- A Chromium based browser, if you don't want to install one just download the latest Ungoogled-Chromium stable archive from [here](https://chromium.woolyss.com/)

## Instructions
1. You need to create a new Bot on Telegram with [BotFather](https://t.me/BotFather), copy and save the ```bot_token```
2. Clone this repo wherever you want to host this project and install dependencies with
```pip install -r requirements.txt```
3. Rename ```config/placeholder_config.json``` and ```users_db/placeholder_links_and_price.json``` to ```config/config.json``` and ```users_db/links_and_price.json```
4. Fill both ```config.json``` and ```links_and_price.json``` with the required values
5. Run ```python pricetracker.py```
6. Enjoy

## How to fill jsons values
If you don't know how to find your Telegram user id just use [this](https://t.me/userinfobot) bot
