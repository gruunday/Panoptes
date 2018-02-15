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
        config = read_config()
        self.sleeptime = config["ping_metrics"]["sleeptime"]

    def read_config(self):
        basepath = path.dirname(__file__)
        config_path = path.abspath(path.join(basepath, "..", "config.json"))
        with open(config_path) as json_config:
            return json.load(json_config)

    # Pings server for the resonce time
    def ping(self):
        ret = subprocess.check_output( \
                ['ping','-W','1','-c','3','145.239.79.126'])
        ret = ret.decode()
        mi, avg, mx, mdev = ret.split()[-2].split('/')
        return mi, avg, mx

    # Overrides run class in Daemon super class
    def run(self):
        while True:
            path = f'\n{platform.node()}.ping.'
            mi, avg, mx = self.ping()

            data = f'{path}min {float(mi)} {time.time()}\n'
            data += f'{path}avg {float(avg)} {time.time()}\n'
            data += f'{path}max {float(mx)} {time.time()}\n'
            self.metric.tcp_fling(data)
            data = ''
            time.sleep(self.sleeptime)
            

# How panoptes controls daemon
def command(order):
    # Create object of class above and run it 
    pinger = Ping_Metric('/tmp/pingMetric.pid')
    if order == 'start':
        return 'Starting'
        pinger.start()
    elif order == 'restart':
        pinger.restart()
        return 'Restarted'
    elif order == 'stop':
        pinger.stop()
        return 'Stopped'
    else:
        sys.exit(2)
