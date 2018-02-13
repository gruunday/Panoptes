#!/usr/bin/env python3.6

from datetime import datetime
import socket
import sys
import time
import pickle
import struct

class Metric_Fling():
    '''
        Class to follow a log file and send metrics to graphite server
    '''
                                # Stub put in config so can be changed easy
                                # If cs is not ip will fail test but work irl
    def __init__(self, cs='145.239.79.126',cp=2003):
        self.carbon_server = cs
        self.carbon_port = cp
        self.addr = (cs, cp)
        
    # Sends message
    def fling(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                  # INET = INTERNET | DGRAM = UDP
        sock.connect(self.addr)
        sock.send(message.encode('utf-8'))
        sock.close()

    # Untested should would if sent with tcp. Pickled is more efficent
    # Should consider moving to this function when things are running smoother
    def pickle_fling(self, data):
        payload = pickle.dumps(data, protocol=2)
        header = struct.pack("!L", len(payload))
        message = header + payload
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, ('145.239.79.126', 2004))
        sock.close()

    # Currently only tcp fling works, udp fling won't work python 3
    def tcp_fling(self, data):
        sock = socket.socket()
        sock.connect(self.addr)
        for metric in data:
            sock.sendall(metric.encode('utf-8'))
        sock.close()
        
    # For testing fling function
    def test_fling(self):
        msg = 'Testing...'
        while True:
            self.fling(msg)
