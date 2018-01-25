"""Test Module; Tests metric_fling daemon."""

sys.path.append("..")
from metric_fling import Metric_Fling
import random
import string
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
    
    def tearDown(self):
        self.flinger.disconnect()

if __name__ == '__main__':
    setUp()
    test_readlog()
    tearDown()
