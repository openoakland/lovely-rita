import os
import os.path as op
import sys
import json


CONFIG_DIRECTORY = op.expanduser('~/.config/lovelyrita')

if not op.exists(CONFIG_DIRECTORY):
    os.makedirs(CONFIG_DIRECTORY)

CONFIG_PATH = op.join(CONFIG_DIRECTORY, 'options.json')
default_config = {'API_KEY': '<<YOUR GOOGLE API KEY>>'}
if not op.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(default_config, f)
        config = default_config
else:
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

API_KEY = config.get('API_KEY', None)
