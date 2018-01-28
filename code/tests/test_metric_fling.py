"""Test Module; Tests metric_fling daemon."""

import os
from metric_fling import Metric_Fling
from multiprocessing.pool import ThreadPool
import threading
import random
from scapy.all import *
import string
import unittest

class Metric_Fling_TestCase(unittest.TestCase):
    """Test Case class for metric_fling daemon"""
    def setUp(self):
        self.flinger = Metric_Fling('/tmp/metricfling.pid', 'test_metric.log')

    def test_readlog(self):
        """Test case A. Can we read log"""
        log = '/tmp/test_metric.log'
        # Gen secret 
        N = random.randint(0,100)
        secret = ''.join(random.choices(string.ascii_uppercase, k=N)) + '\n'
        # Start thread to write while we listen
        write = threading.Thread(target=self.writer, args=(log, secret))
        write.start()
        # Listen for secret
        f = open(log, 'r')
        secret_file = self.flinger.follower(f)
        for return_secret in secret_file:
            self.assertEqual(secret, return_secret, \
                                'Read of file was not equal to what was written')
            break
        f.close()
   
    # Helper to write secret to log file
    def writer(self, log, secret):
        for _ in range(20):
            f = open(log, 'w+')
            f.write(secret)
            print('wrote')
            f.close()

    def test_fling_ip(self):
        """Test Case B. IP correct dest"""
        pool = ThreadPool(processes=1)
        dest = pool.apply_async(self.flinger.test_fling)
        pkt = sniff(filter='udp and host 145.239.79.126', count=1)
        real_dst = pkt[0][IP].dst
        self.assertEqual('145.239.79.126', real_dst, \
                            'Desination of metric is wrong')
 
    def test_fling_port(self):
        """Test Case C. Port correct dest port"""
        pool = ThreadPool(processes=1)
        dest = pool.apply_async(self.flinger.test_fling)
        pkt = sniff(filter='udp and host 145.239.79.126', count=1)
        real_port = pkt[0][UDP].dport
        self.assertEqual(self.flinger.carbon_port, real_port, \
                            'Desination port of metric is wrong is {real_port}')


    def tearDown(self):
        self.flinger.disconnect()
        try:
            os.remove('test_metric.log')
        except FileNotFoundError:
            pass # Explicitly silent

if __name__ == '__main__':
    setUp()
    test_readlog()
    test_fling_ip()
    test_fling_port()
    tearDown()
