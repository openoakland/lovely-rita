import os
import os.path as op
import shutil
import json

import lovelyrita

DEFAULT_CONFIG_PATH = op.join(op.dirname(lovelyrita.__file__), 'options.json')

CONFIG_DIRECTORY = op.expanduser('~/.config/lovelyrita')

if not op.exists(CONFIG_DIRECTORY):
    os.makedirs(CONFIG_DIRECTORY)

CONFIG_PATH = op.join(CONFIG_DIRECTORY, 'options.json')
default_config = {'API_KEY': '<<YOUR GOOGLE API KEY>>'}
if not op.exists(CONFIG_PATH):
    shutil.copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

GOOGLE_API_KEY = config.get('GOOGLE_API_KEY', None)
GOOGLE_API_URL = config.get('GOOGLE_API_URL', None)

POSTGIS_HOST = config.get('POSTGIS_HOST', 'localhost')
POSTGIS_PORT = config.get('POSTGIS_PORT', '5432')
POSTGIS_DATABASE = config.get('POSTGIS_DATABASE', 'postgres')
POSTGIS_USERNAME = config.get('POSTGIS_USERNAME', 'postgres')
POSTGIS_PASSWORD = config.get('POSTGIS_PASSWORD', '')
