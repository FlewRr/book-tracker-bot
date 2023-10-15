## Book tracking bot for your books

Welcome! This is bot for keeping information about your read/planned books. Bot was made in Python on aiogram with usage of sqlalchemy for databases and poetry for dependencies management.


# Usage
Basically, bot has 3 main functions:      
  1. Add/Remove book to/from your lists (read list and planned list).
  2. Rate the book that is already in the list.
  3. Get full content of your lists.

How to use it:    
  * To start the bot use /start command.
  * Choose what you'd like to do and press the right button.
  * To add/remove book use add/remove buttons.
  * To get content of lists use read/planned button.
  * To set rating to the book use rate button then follow instructions of the bot.
  * If you misclicked you always can come back with back button.

# Installation

* Clone this repository to your local machine
```
git clone https://github.com/FlewRr/book-tracker-bot
```
* Create your bot with [BotFather](https://t.me/botfather) and paste its api token into the bot/resources/config.json

* Install [poetry](https://python-poetry.org/docs/)
```
curl -sSL https://install.python-poetry.org | python3 -
```
* Install environment (terminal shall be opened in the folder with poetry.lock file)
```
poetry install
```

* Run bot
```
poetry run python bot/main.py
```


# Notes
  I'd appreciate any feedback so feel free to contact me if you have any question or just want to help. 
