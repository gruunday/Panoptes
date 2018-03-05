# !/usr/bin/env python3.6

import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
import platform
from os import path
import json
import time

class System_Stats(Daemon):
    '''
        Class to monitor system stats
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
        self.metric = Metric_Fling()
        config = self.read_config()
        self.errorlog = config["system_stats"]["errorlog"]
        self.sleeptime = config["system_stats"]["sleeptime"]

    def read_config(self):
        """
        Read in config values from json config to set configurable variables
        """
        basepath = path.dirname(__file__)
        config_path = path.abspath(path.join(basepath, "..", "config.json"))
        with open(config_path) as json_config:
            return json.load(json_config)

    def get_loadavg(self):
        """
        Reads /proc/loadavg file to find the systems load average for 1min 5min 10min

        :raises OSError: file could not be read
        """
        try:
            f = open('/proc/loadavg', 'r')
            data = f.read().strip().split()[:3]
            f.close()
        except OSError as e:
            f = open(self.errorlog, 'a+')
            f.write('{time.time()} {e}')
            f.close
        return data

    def parse(self, data):
        """
        Formats data recived from file to graphite metric format

        :data: list of strings to be formatted
        """
        path = f'\n{platform.node()}.system.loadavg.'
        loadagv_metric_string = f'{path}1min {data[0]} {time.time()}\n'
        loadagv_metric_string += f'{path}5min {data[1]} {time.time()}\n'
        loadagv_metric_string += f'{path}10min {data[2]} {time.time()}\n'
        return loadagv_metric_string

    def run(self):
        """
        Runs the daemon controls funcitonality
        """
        while True:
            data = self.get_loadavg()
            data = self.parse(data)
            self.metric.tcp_fling(data)
            time.sleep(self.sleeptime)

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
