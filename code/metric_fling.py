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
    def __init__(self, lf, cs = '145.239.79.126', cp = 2003):
        self.carbon_server = cs
        self.carbon_port   = cp
        self.log_file      = lf
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                  # INET = INTERNET | DGRAM = UDP
        
    # Sends message
    def fling(self, message):
        self.sock.sendto(bytes(message, "utf-8"), \
                            (self.carbon_server, self.carbon_port))

    # Disconnect from server
    def disconnect(self):
        self.sock.close()

    # For testing fling function
    def test_fling(self):
        while True:
            self.fling('Testing...')
