"""
Manage all the settings config here
"""
import os
from typing import List, NamedTuple

from dotenv import load_dotenv


load_dotenv()

class SettingsConfig(NamedTuple) :
    DB_URL: str
    TITLE: str
    VERSION: str
    DESCRIPTION: str
    CONTACT: List[dict]

settings_config = {
    'DB_URL' : 'postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'.format(
        DB_USER = os.getenv('DB_USER'),
        DB_PWD = os.getenv('DB_PWD'),
        DB_HOST = os.getenv('DB_HOST'),
        DB_PORT = os.getenv('DB_PORT'),
        DB_NAME = os.getenv('DB_NAME')
    ),
    'TITLE' : 'OCruxCards',
    'VERSION' :'0.0.1',
    'DESCRIPTION' : '',
    'CONTACT' : [{
        'name' : 'Nishant',
        'email' : 'nishant7.ng@gmail.com',
    }],

}

settings = SettingsConfig(**settings_config)

if __name__ == '__main__':
    print(settings)
