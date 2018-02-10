"""Test System Stats; testing system stats"""

import unittest
from plugins.system_stats import System_Stats
from plugins.system_stats import command

class System_Stats_TestCase(unittest.TestCase):
    """Test System Stats"""

    def setUp(self):
        self.stater = System_Stats('/tmp/systemStats.pid')
        f = open('/proc/loadavg', 'r')
        self.data = f.read().strip().split()[:3]
        f.close()

    def test02_get_loadavg(self):
        """Test get loadavg"""
        load = self.stater.get_loadavg()
        self.assertEqual(self.data, load)

    def test03_parse(self):
        """Test parse function"""
        parsed_data = self.stater.parse(self.data)
        self.assertEqual(len(parsed_data.split('\n\n')), 3)
        self.assertEqual(len(parsed_data.split()), 9)

    def test04_nodes_up_start(self):
        """Test system stats start"""
        ans = command('start')
        self.assertEqual('Starting', ans)

    def test05_nodes_up_restart(self):
        """Test system stats restart"""
        #with self.assertRaises(SystemExit) as cm:
        #    command('restart')
        #self.assertEqual(cm.exception.code, 0)
        ans = command('restart')
        self.assertEqual('Restarted', ans)

    def test06_nodes_up_stop(self):
        """Test system stats stop"""
        ans = command('stop')
        self.assertEqual('Stopped', ans)

    def test07_unknown_command(self):
        """Test system stats bad command"""
        with self.assertRaises(SystemExit) as cm:
            command('hooglety boodlety')
        self.assertEqual(cm.exception.code, 2)
