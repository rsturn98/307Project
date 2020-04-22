# 307Project
COMP 307 Final Project - Game Topic

## Group Members
Tristan Sigurdsson-Morris 260830362 <br />
Lukas Shannon 260616276 <br />
Rachel Sturn 260707106 <br />

## Installation

Assuming you already have Django, install the following libraries

https://github.com/django/channels_redis 

```bash

pip install -U channels
pip install channels_redis Django
pip install stripe

```

## Usage

From a python environment go into mysite folder that contains manage.py and run 'python manage.py runserver'.
Go to localhost:8000/ to begin.
To make a payment, use credit card number 4242 4242 4242 4242.
Open two different accounts in different browsers.
Have one user start a new game room, then the second user. Join the game room with the same name (will appear under 'Looking for Challenger' dropdown, or can enter the same room name in the text input). The game will then be shown under the "In Progress" dropdown.
The game begins when both users have selected their powers.

## Playing the game

Click the button associated with the action you want to take. Once both players have sent their actions, the game server will resolve the turn and send to each client the adjusted game state as well as posting a description of the turn in the game chat.
When one player gets to 0 or less HP remaining, the game will end and set the winning player, visible in each player's game history. The game will now be shown in the "Completed" dropdown.
...
