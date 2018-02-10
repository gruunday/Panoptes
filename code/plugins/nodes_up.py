# !/usr/bin/env python3.6

import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
import platform
import time

class Nodes_Up(Daemon):
    '''
        Class to monitor nodes running
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
        self.metric = Metric_Fling()

    def run(self):
        while True:
            metric = f'\n{platform.node()}.isup 1 {time.time()}\n' 
            self.metric.fling(metric)
            time.sleep(60)

# How panoptes controls daemon
def command(order):
    stats = Nodes_Up('/tmp/nodesUp.pid')
    if 'start' == order:
        return 'Starting'
        stats.start()
    elif 'restart' == order:
        stats.restart()
        return 'Restarted'
    elif 'stop' == order:
        stats.stop()
        return 'Stopped'
    else:
        sys.exit(2)

