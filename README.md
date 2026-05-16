# SydSocialBasketball-ICS-Generator

## Features
* Generate an ICS based on your team

### Not Yet Implemented
* Alert when your schedule changes
* Generate an ICS based on your account

## Installation and Running
I've used pipenv but you can run it in venv if you'd like

1. `git clone git@github.com:KristianMansfield/SydSocialBasketball-ICS-Generator.git && cd SydSocialBasketball-ICS-Generator`
1. `pipenv install`
1. `pipenv run python3 main.py`
1. Upload the generated ics file to your calendar app.

## How It Works
1. Prompt user for a team URL
1. Download schedue for that team
1. Convert to ICS & download
1. User uploads to calendar app