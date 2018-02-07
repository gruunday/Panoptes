# !/usr/bin/env python3.6

import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
import platform
import time

class System_Stats(Daemon):
    '''
        Class to monitor system stats
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
        self.metric = Metric_Fling()

    def run(self):
        while True:
            metric = f'\n{platform.node()}.isup 1 {time.time()}\n' 
            self.metric.tcp_fling(metric)
            time.sleep(30)

# How panoptes controls daemon
def command(order):
    stats = System_Stats('/tmp/systemStats.pid')
    if 'start' == order:
        return 'Starting'
        stats.start()
    elif 'restart' == order:
        return 'Restarted'
        stats.restart()
    elif 'stop' == order:
        stats.stop()
        return 'Stopped'
    else:
        return 'Command Unknown'
        sys.exit(2)

if __name__ == '__main__':
    stats = System_Stats('/tmp/systemStats.pid')
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1].lower():
            print('Starting')
            stats.start()
        elif 'restart' == sys.argv[1].lower():
            print('Restarted')
            stats.restart()
        elif 'stop' == sys.argv[1].lower():
            stats.stop()
            print('Stopped')
        else:
            print('Command Unknown')
            sys.exit(2)
    else:
        print(f'Usage: {sys.argv[0]} start|stop|restart')
        sys.exit(2)
