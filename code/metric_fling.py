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
        """
        Takes a metric string and sends it to graphite server with UDP

        :message: string metric to be sent to graphite server
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                  # INET = INTERNET | DGRAM = UDP
        sock.connect(self.addr)
        sock.send(message.encode('utf-8'))
        sock.close()

    # Untested should would if sent with tcp. Pickled is more efficent
    # Should consider moving to this function when things are running smoother
    def pickle_fling(self, data):
        """
        Take a metric list of strings and pickles them before sending to graphite server with TCP

        :data: a list of strings to be pickled and sent
        """
        payload = pickle.dumps(data, protocol=2)
        header = struct.pack("!L", len(payload))
        message = header + payload
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, ('145.239.79.126', 2004))
        sock.close()

    # Currently only tcp fling works, udp fling won't work python 3
    def tcp_fling(self, data):
        """
        take a metric string and send it ro graphite server with TCP

        :data: strings to be sent to grapite server
        """
        sock = socket.socket()
        connected = False
        while not connected:
            try:
                sock.connect(self.addr)
                connected = True
            except Excepion as e:
                with open('/var/log/panoptes/system.log', 'a+') as f:
                    f.write('Connecting with metric fling had problems {e}\n')
                sys.exit(758)
        for metric in data:
            sock.sendall(metric.encode('utf-8'))
        sock.close()
        
    # For testing fling function
    def test_fling(self):
        """
        Used for testing the fling funtions
        """
        msg = 'Testing...'
        while True:
            self.fling(msg)
