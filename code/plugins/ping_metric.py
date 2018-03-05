# !/usr/bin/env python3.6

import sys
# Import the folder above 
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
import scapy
import platform
import subprocess
from os import path
import json
import time

class Ping_Metric(Daemon):
    '''
        Test latecy in network
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
        self.metric = Metric_Fling()
        config = self.read_config()
        self.sleeptime = config["ping_metrics"]["sleeptime"]

    def read_config(self):
        """
        Reads config from json files and sets configurable vaiables
        """
        basepath = path.dirname(__file__)
        config_path = path.abspath(path.join(basepath, "..", "config.json"))
        with open(config_path) as json_config:
            return json.load(json_config)

    # Pings server for the resonce time
    def ping(self):
        """
        Requests ping from os and returns times
        """
        try:
            ret = subprocess.check_output( \
                ['ping','-W','1','-c','3','145.239.79.126'])
            ret = ret.decode()
            mi, avg, mx, mdev = ret.split()[-2].split('/')
        except subprocess.CalledProcessError:
            # This error will occur because the script has not connected
            # to the internet. This is fine and expected
            pass
        return mi, avg, mx

    # Overrides run class in Daemon super class
    def run(self):
        """
        Runs the daemon and controls execution
        """
        while True:
            path = f'\n{platform.node()}.ping.'
            try:
                mi, avg, mx = self.ping()
                data = f'{path}min {float(mi)} {time.time()}\n'
                data += f'{path}avg {float(avg)} {time.time()}\n'
                data += f'{path}max {float(mx)} {time.time()}\n'
                self.metric.tcp_fling(data)
                data = ''
                time.sleep(self.sleeptime)
            except Exception:
                pass

if __name__ == '__main__':
    order = sys.argv[1]
    pinger = Ping_Metric('/tmp/pingMetric.pid')
    if order == 'start':
        pinger.start()
        print('Starting')
    elif order == 'restart':
        pinger.restart()
        print('Restarting')
    elif order == 'stop':
        pinger.stop()
        print('Stoping')
    else:
        print('Bad argument given')
        sys.exit(2)
