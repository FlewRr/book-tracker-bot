import json
from pydantic import BaseModel


class BotConfig(BaseModel):
    token : str


class Messages(BaseModel):
    welcome : str
    about : str
    help : str
    add : str
    remove : str
    off : str


class Buttons(BaseModel):
    add : str
    remove : str
    read : str
    planned : str
    back : str


class BotSettings:

    _map = dict()
    _messages_path = "bot/resourses/messages.json"
    _config_path = "bot/resourses/config.json"
    _buttons_path = "bot/resourses/buttons.json"
    
    def __init__(self):
        self.load()
    
    @property
    def config(self) -> BotConfig:
        return self._map['config']
    
    @property
    def messages(self) -> Messages:
        return self._map['messages']
    
    @property
    def buttons(self) -> Buttons:
        return self._map['buttons']

    def load(self):
        
        with open(self._config_path) as f:
            self._map['config'] = BotConfig(**json.load(f))
        with open(self._messages_path) as f:
            self._map['messages'] = Messages(**json.load(f))
        with open(self._buttons_path) as f:
            self._map['buttons'] = Buttons(**json.load(f))

if __name__ == "__main__":
    bot_settings = BotSettings()
    print(bot_settings.config)
    print(bot_settings.messages)
    print(bot_settings.buttons)
