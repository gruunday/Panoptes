import sys
import json

slack_token = sys.argv[1]
pushbullet_token = sys.argv[2]
pushbullet2_token = sys.argv[3]

with open('config.json', 'r') as json_config:
    config = json.load(json_config)

config["slack"]["slack_token"] = slack_token
config["pushbullet"]["push_device_tokens"] = [pushbullet_token, pushbullet2_token]

with open('config.json', 'w') as json_config:
    json.dump(config, json_config)
