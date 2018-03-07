#!/usr/bin/env python3.6

from slackclient import SlackClient
from pushbullet import Pushbullet
import json

class Alert():

    def __init__(self):
        config = self.read_config()
        self.slack_token = config["slack"]["slack_token"] 
        self.slack_channel = config["slack"]["slack_channel"] 
        self.slack_username = config["slack"]["slack_username"] 
        self.slack_emoji = config["slack"]["slack_emoji"]
        self.push_tokens = config["pushbullet"]["push_device_tokens"]

    def read_config(self):
        with open('config.json') as json_config:
            return json.load(json_config)

    def _slack_alert(self, message):
        sc = SlackClient(self.slack_token)
        sc.api_call('chat.postMessage', channel=self.slack_channel, 
                    text=message, username=self.slack_username,
                    icon_emoji=self.slack_emoji)
	
    def _pushbullet_alert(self, message):
        if self.push_tokens[0] != "insert api tokens":
            for token in self.push_tokens:
                Pushbullet(token).push_note("Alert", message)
		

def send_alert(message):
    alert = Alert()
    alert._slack_alert(message)
    alert._pushbullet_alert(message)
