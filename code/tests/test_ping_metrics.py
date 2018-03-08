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
        while True:
            ret_min, ret_avg, ret_max = self.pinger.ping()
            if ret_min != None:
                 break
        self.assertEqual(isinstance(float(ret_min), float), True, f'{ret_min}, {type(ret_min)}')
        self.assertEqual(isinstance(float(ret_avg), float), True)
        self.assertEqual(isinstance(float(ret_max), float), True)
        self.assertLess(ret_min, ret_avg)
        self.assertLess(ret_avg, ret_max)
        self.assertLess(ret_min, ret_max)
 
    def test_read_config(self):
        """Test Case B. Read Config performs correctly"""
        config = self.pinger.read_config()
        self.assertEqual(config, self.config)
