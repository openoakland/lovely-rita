import os
import json
from pathlib import Path

import appdirs

import lovelyrita

CONFIG_DIRECTORY = Path(appdirs.user_config_dir()) / 'lovelyrita'
CONFIG_DIRECTORY.mkdir(exist_ok=True)
CONFIG_PATH = CONFIG_DIRECTORY / 'options.json'

if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

else:
    config = {}

GOOGLE_API_KEY = config.get('GOOGLE_API_KEY', None)
GOOGLE_API_URL = config.get('GOOGLE_API_URL', None)

POSTGIS_HOST = config.get('POSTGIS_HOST', 'localhost')
POSTGIS_PORT = config.get('POSTGIS_PORT', '5432')
POSTGIS_DATABASE = config.get('POSTGIS_DATABASE', 'postgres')
POSTGIS_USERNAME = config.get('POSTGIS_USERNAME', 'postgres')
POSTGIS_PASSWORD = config.get('POSTGIS_PASSWORD', '')

VALID_COLUMN_NAMES = config.get('VALID_COLUMN_NAMES', [])

DATETIME_FORMATS = ['%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M', '%Y-%m-%d %H:%M']
