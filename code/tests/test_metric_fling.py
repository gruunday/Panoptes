"""Test Module; Tests metric_fling daemon."""

import os
from metric_fling import Metric_Fling
from multiprocessing.pool import ThreadPool
from scapy.all import *
import unittest

class Metric_Fling_TestCase(unittest.TestCase):
    """Test Case class for metric_fling daemon"""
    def setUp(self):
        self.flinger = Metric_Fling()

    def test_fling_ip(self):
        """Test Case A. IP correct dest"""
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

