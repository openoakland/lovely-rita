import os
import os.path as op
import json

import lovelyrita

DEFAULT_CONFIG_PATH = op.join(op.dirname(lovelyrita.__file__), 'options.json')

with open(DEFAULT_CONFIG_PATH, 'r') as f:
    config = json.load(f)

CONFIG_DIRECTORY = op.expanduser('~/.config/lovelyrita')

if not op.exists(CONFIG_DIRECTORY):
    os.makedirs(CONFIG_DIRECTORY)

CONFIG_PATH = op.join(CONFIG_DIRECTORY, 'options.json')

if not op.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'w') as f:
        json.dump({}, f)

with open(CONFIG_PATH, 'r') as f:
    user_config = json.load(f)

config.update(user_config)

GOOGLE_API_KEY = config.get('GOOGLE_API_KEY', None)
GOOGLE_API_URL = config.get('GOOGLE_API_URL', None)

POSTGIS_HOST = config.get('POSTGIS_HOST', 'localhost')
POSTGIS_PORT = config.get('POSTGIS_PORT', '5432')
POSTGIS_DATABASE = config.get('POSTGIS_DATABASE', 'postgres')
POSTGIS_USERNAME = config.get('POSTGIS_USERNAME', 'postgres')
POSTGIS_PASSWORD = config.get('POSTGIS_PASSWORD', '')

VALID_COLUMN_NAMES = config.get('VALID_COLUMN_NAMES', [])

DATETIME_FORMATS = ['%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M', '%Y-%m-%d %H:%M']
