## Book tracking bot

Welcome! This is bot for keeping information about your read/planned books. Bot was made in Python with usage of aiogram and sqlalchemy.


# Usage
Basically, bot has 3 main functions:      
  1. Add/Remove book to/from your lists (read list and planned list).
  2. Rate the book that is already in the list.
  3. Get full content of your lists.
  4. Get recommendations based on your books.

How to use it:    
  * To start the bot use /start command.
  * Choose what you'd like to do and press the right button.
  * To add/remove book use add/remove buttons.
  * To get content of lists use read/planned button.
  * To set rating to the book use rate button then follow instructions of the bot.
  * Command /recs returns list of recommendations based on user's books.
  * If you misclicked you always can come back with back button.
  * You can use command /help or /about to get understanding of what bot is capable of.
  * You can use command /recs to get recommendations based on your reading lists.
# Installation

* Clone this repository
```
git clone https://github.com/FlewRr/book-tracker-bot
```
* Create your bot with [BotFather](https://t.me/botfather) and paste its api token into the bot/resources/config.json

* Install requirements in the root folder
```
pip install -r requirements.txt
```

* Create db (may take around one minute)
```
python3 bot/create_db.py
```

* Run bot
```
python3 bot/main.py
```

# Recommendation System
Recsys model is written with usage of [Approximate Nearest Neighbours](https://github.com/spotify/annoy) which is C++ library with Python bindings to search for points in space that are close to a given query point.
Model architecture can be described as:
  * User's interactions and opensource data (since bot is not popular enough to generate sufficient amount of data) are stored in sqlite3 database.
  * After User's request all the data is factorized into mappings of users interactions and its features.
  * After that AnnoyRecommender which is based on [annoy library]((https://github.com/spotify/annoy)) is fit with mappings.
  * AnnoyRecommender generates recommendations for user and sends it to them.
