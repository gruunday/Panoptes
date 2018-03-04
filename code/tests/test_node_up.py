"""Test Module; Tests alert system"""

import os
from time import strftime
from plugins.nodes_up import Nodes_Up
import time
import unittest

class Nodes_Up_TestCase(unittest.TestCase):
    """Test Nodes Up"""
    def setUp(self):
        self.stats = Nodes_Up('/tmp/nodesUp.pid')
    
    def test01_nodes_up_start(self):
        """Test Nodes up start"""
        with self.assertRaises(SystemExit) as ex:
            self.stats.start()
        self.assertEqual(ex.exception.code, 0)
 
    def test02_nodes_up_restart(self):
        """Test Nodes up restart"""
        with self.assertRaises(SystemExit) as cm:
            self.stats.stop()
            self.stats.start()
        self.assertEqual(cm.exception.code, 0)
   
    def test03_nodes_up_stop(self):
        """Test Nodes stop"""
        self.stats.stop()

    def tearDown(self):
        self.stats.stop()
