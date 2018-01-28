"""Test Module; Tests metric_fling daemon."""

import os
import subprocess as sp
import random 
from time import strftime
from metric_fling import Metric_Fling
import unittest

class Metric_Fling_TestCase(unittest.TestCase):
    """Test Case class for metric_fling daemon"""
    def setUp(self):
        f = open('/tmp/metrix.log', 'a+')
        for _ in range(20):
            f.write(f'fake.metrics.local {random.randint(0,100)} {strftime("%H:%M:%S")}')
        f.close()

    def test_solo_start(self):
        """Test Case D Solo metric fling startup"""
        # Start system 
        os.system('python3.6 metric_fling.py start')
        aux_out = str(sp.check_output(['ps','aux'])).count('python3.6 metric_fling.py')
        self.assertGreaterEqual(aux_out, 1, 'Start test failed')

        # Restart system
        os.system('python3.6 metric_fling.py restart')
        aux_out = str(sp.check_output(['ps','aux'])).count('python3.6 metric_fling.py')
        self.assertGreaterEqual(aux_out, 1, 'Restart test failed')

        # Stop system
        os.system('python3.6 metric_fling.py stop')
        aux_out = str(sp.check_output(['ps','aux'])).count('python3.6 metric_fling.py')
        self.assertEqual(aux_out, 0, 'Stop test failed')

if __name__ == '__main__':
    test_solo_start()