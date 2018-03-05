# !/usr/bin/env python3.6

import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
import platform
from os import path
import time
import json

class Nodes_Up(Daemon):
    '''
        Class to monitor nodes running
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
        self.metric = Metric_Fling()
        config = self.read_config()
        self.sleeptime = config["nodeup"]["sleeptime"]

    def read_config(self):
        """
        Reads a json config to set configuable variables
        """
        basepath = path.dirname(__file__)
        config_path = path.abspath(path.join(basepath, "..", "config.json"))
        with open(config_path) as json_config:
            return json.load(json_config)

    def run(self):
        """
        Starts the daemons
        """
        while True:
            metric = f'\n{platform.node()}.isup 1 {time.time()}\n' 
            self.metric.tcp_fling(metric)
            time.sleep(self.sleeptime)

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        order = sys.argv[1]
        stats = Nodes_Up('/tmp/nodesUp.pid')
        if 'start' == order:
            print('Starting')
            stats.start()
        elif 'restart' == order:
            stats.restart()
            print('Restarted')
        elif 'stop' == order:
            stats.stop()
            print('Stopped')
        else:
            print('Unknown command given')
            sys.exit(2)
    else:
        print('No command given')
        sys.exit(2)
