import sys
import json

token = sys.argv[1]
with open('config.json', 'r') as json_config:
    config = json.load(json_config)

config["slack"]["slack_token"] = token

with open('config.json', 'w') as json_config:
    json.dump(config, json_config)
