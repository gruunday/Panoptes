#!/usr/bin/env python3.6

from datetime import datetime
import socket
import sys
import time

class Metric_Fling():
    '''
        Class to follow a log file and send metrics to graphite server
    '''
                                # Stub put in config so can be changed easy
                                # If cs is not ip will fail test but work irl
    def __init__(self, cs='panoptes.xyz',cp=2003):
        self.addr = (cs, cp)
                                  # INET = INTERNET | DGRAM = UDP
        
    # Sends message
    def fling(self, message):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect(('panoptes.xyz', 2003))
        self.sock.sendall(message.encode('utf-8'))
        self.sock.close()

    # Disconnect from server
    def disconnect(self):
        self.sock.close()

    # For testing fling function
    def test_fling(self):
        while True:
            self.fling('Testing...')
