#!/usr/bin/env python3.6

from slackclient import SlackClient
from config import slack_token, slack_channel

def slack_alert(message, channel=slack_channel):
    sc = SlackClient(slack_token)
    sc.api_call('chat.postMessage', channel=channel, 
                text=message, username='Panoptes Alerts',
                icon_emoji=':robot_face:')
