"""Test Module; Tests metric_fling daemon."""

import os
import sys
sys.path.append("..")
from metric_fling import Metric_Fling
import random
import string
from scapy.all import *
import unittest

class readmeTestCase(unittest.TestCase):
    """Test Case class for metric_fling daemon"""
    def setUp(self):
        self.flinger = Metric_Fling('/tmp/metricfling.pid', 'test_metric.log')

    def test_readlog(self):
        """Test case A. Can we read log"""
        N = random.randint(0,100)
        secret = ''.join(random.choices(string.ascii_uppercase, k=N))
        f = open('test_metric.log', 'w+')
        f.write(secret)
        return_secret = self.flinger.follower(f)
        f.close()
        self.assertNotEqual(secret, return_secret, \
                            'Read of file was not equal to what was written')

    def sniffer(self):
        yield sniff(filter='udp', count=1)

    def test_fling_ip(self):
        pkt = self.sniffer()
        while not pkt:
           self.flinger.fling('testing...')
        real_dst = pkt[0][IP].dst
        self.assertEqual('145.239.79.126', real_dst, \
                            'Desination of metric is wrong')
 
    def test_fling_port(self):
        pkt = self.sniffer()
        while not pkt:
            self.flinger.fling('testing...')
        real_port = pkt[0][UDP].dport
        self.assertEqual('2003', real_port, \
                            'Destination port for metric is wrong')   
    
    def tearDown(self):
        self.flinger.disconnect()
        try:
            os.remove('test_metric.log')
        except FileNotFoundError:
            pass # Explicitly silent

if __name__ == '__main__':
    setUp()
    test_fling_ip()
    test_fling_port()
    test_readlog()
    tearDown()
