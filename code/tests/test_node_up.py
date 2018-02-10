"""Test Module; Tests alert system"""

import os
from time import strftime
from plugins.nodes_up import command
import time
import unittest

class Nodes_Up_TestCase(unittest.TestCase):
    """Test Nodes Up"""
    def test_nodes_up_start(self):
        """Test Nodes up start"""
        ans = command('start')
        self.assertEqual('Starting', ans)
 
    def test_nodes_up_start(self):
        """Test Nodes up restart"""
        with self.assertRaises(SystemExit) as cm:
            command('restart')
        self.assertEqual(cm.exception.code, 0)
   
    def test_nodes_up_stop(self):
        """Test Nodes stop"""
        ans = command('stop')
        self.assertEqual('Stopped', ans)

    def test_unknown_command(self):
        """Test Nodes up bad command"""
        with self.assertRaises(SystemExit) as cm:
            command('hoogle boodle')
        self.assertEqual(cm.exception.code, 2)
