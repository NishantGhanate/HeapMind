"""
Manage all the settings config here
"""
import os
from typing import List, NamedTuple, Optional

from dotenv import load_dotenv
import pytz


load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
RABBIT_URL = os.getenv('RABBIT_URL')

class SettingsConfig(NamedTuple) :
    DB_URL: str
    TITLE: str
    VERSION: str
    DESCRIPTION: str
    CONTACT: List[dict]
    REDIS_URL: str
    RABBIT_URL: str
    TIMEZONE: Optional[str]
    LOGGER_NAME: str = 'heap_mind'


    @property
    def tzinfo(self):
        return pytz.timezone(self.TIMEZONE)

    @property
    def logger(self):
        return self.LOGGER_NAME

settings_config = {
    'DB_URL' : f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    'TITLE' : 'HeapMind',
    'VERSION' :'0.0.1',
    'DESCRIPTION' : '',
    'CONTACT' : [{
        'name' : 'Nishant',
        'email' : 'nishant7.ng@gmail.com',
    }],
    "REDIS_URL": os.getenv('REDIS_URL'),
    'RABBIT_URL': os.getenv('RABBIT_URL'),
    'TIMEZONE': os.getenv('TIMEZONE')
}

settings_config = SettingsConfig(**settings_config)
