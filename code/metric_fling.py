#!/usr/bin/env python3.6

from daemon import Daemon
from datetime import datetime
import socket
import sys
import time

class Metric_Fling(Daemon):
    '''
        Class to follow a log file and send metrics to graphite server
    '''
                                # Stub put in config so can be changed easy
    def __init__(self, pidf, lf, cs = '145.239.79.126', cp = 2003):
        Daemon.__init__(self, pidf)
        self.carbon_server = cs
        self.carbon_port   = cp
        self.log_file      = lf
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                  # INET = INTERNET | DGRAM = UDP
        
    # Sends message
    def fling(self, message):
        self.sock.sendto(bytes(message, "utf-8"), \
                            (self.carbon_server, self.carbon_port))

    # Disconnect from server
    def disconnect(self):
        self.sock.close()

    # For testing fling function
    def test_fling(self):
        while True:
            self.fling('Testing...')

    # Follow a log file like tail -f
    def follower(self, f):
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def run(self):
        try:
            lf = open(self.log_file, 'r')
        except FileNotFoundError as e:
            sys.stdout.write(f'\n\n\nFileNotFound: {e}\n')
            sys.exit(1)
        loglines = self.follower(lf)
        for metric in loglines:
            self.fling(metric)
        
if __name__ == '__main__':
                                # STUB | Hardcoded log file, should change
    metric_fling = Metric_Fling('/tmp/metricfling.pid', '/tmp/metrix.log')
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1].lower():
            metric_fling.start()
            print('Started')
        elif 'restart' == sys.argv[1].lower():
            metric_fling.restart()
            print('restarted')
        elif 'stop' == sys.argv[1].lower():
            metric_fling.stop()
            print('Stopped')
        else:
            print('Command Unknown')
            sys.exit(2)
    else:
        print(f'Usage: {sys.argv[0]} start|stop|restart')
        sys.exit(2)
