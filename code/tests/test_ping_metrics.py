"""Test Module; Tests metric_fling daemon."""

import json
import os
from os import path
from plugins.ping_metric import Ping_Metric
import unittest

class Metric_Fling_TestCase(unittest.TestCase):
    """Test Case class for metric_fling daemon"""
    def setUp(self):
        self.pinger = Ping_Metric('/tmp/pingMetric.pid')
        self.config = self.read_config()

    def read_config(self):
        """Reads in json config files and sets configurable variables"""
        basepath = path.dirname(__file__)
        config_path = path.abspath(path.join(basepath, "..", "config.json"))
        with open(config_path) as json_config:
            return json.load(json_config)

    def test_ping(self):
        """Test Case A. Ping performs correctly"""
        ret_min, ret_avg, ret_max = self.pinger.ping()
        self.assertEqual(isinstance(ret_min, int), True)
        self.assertEqual(isinstance(ret_avg, int), True)
        self.assertEqual(isinstance(ret_max, int), True)
        self.assertLess(ret_min, ret_avg)
        self.assertLess(ret_avg, ret_max)
        self.assertLess(ret_min, ret_max)
 
    def test_read_config(self):
        """Test Case B. Read Config performs correctly"""
        config = self.pinger.read_config()
        self.assertEqual(config, self.config)

