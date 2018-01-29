"""Test Module; Tests alert system"""

import os
import subprocess as sp
import random 
from time import strftime
from alert import slack_alert
import unittest

class Metric_Fling_TestCase(unittest.TestCase):
    """Test Case class for alerts"""
    def test_alert(self):
        """Test Case D Alerts"""
        slack_alert('Build Testing Alerts')

if __name__ == '__main__':
    test_alert()
