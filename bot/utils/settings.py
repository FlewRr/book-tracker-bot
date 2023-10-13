import json
from pydantic import BaseModel


class BotConfig(BaseModel):
    token : str


class Messages(BaseModel):
    welcome : str
    about : str
    help : str
    add : str
    delete : str
    off : str


class BotSettings:

    _map = dict()
    _messages_path = "bot/resourses/messages.json"
    _config_path = "bot/resourses/config.json"

    def __init__(self):
        self.load()
    
    @property
    def config(self) -> BotConfig:
        return self._map['config']
    
    @property
    def messages(self) -> Messages:
        return self._map['messages']
    

    def load(self):
        
        with open(self._config_path) as f:
            self._map['config'] = BotConfig(**json.load(f))
        with open(self._messages_path) as f:
            self._map['messages'] = Messages(**json.load(f))


if __name__ == "__main__":
    bot_settings = BotSettings()
    print(bot_settings.config)
    print(bot_settings.messages)