# !/usr/bin/env python3.6

import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
from scapy.all import *
import subprocess
import platform
from os import path
import json

class Packet_Stats(Daemon):
    '''
        Class to collect stats about packets
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
        config = self.read_config()
        self.metric = Metric_Fling()
        self.timeout = config["packet_stats"]["timeout"]
        self.iface = config["packet_stats"]["interface"]

    def read_config(self):
        """
        Reads in json config and sets configurable variables
        """
        basepath = path.dirname(__file__)
        config_path = path.abspath(path.join(basepath, "..", "config.json"))
        with open(config_path) as json_config:
            return json.load(json_config)

    def parse_metrics(self, tcp, udp, icmp, other):
        """
        Formats and send metrics to graphite server
        """
        metric = []
        metric.append(f'\n{platform.node()}.pkt.tcp {tcp} {time.time()}\n')
        metric.append(f'\n{platform.node()}.pkt.udp {udp} {time.time()}\n')
        metric.append(f'\n{platform.node()}.pkt.icmp {icmp} {time.time()}\n')
        metric.append(f'\n{platform.node()}.pkt.other {other} {time.time()}\n')
        self.metric.tcp_fling(metric)

    def find_ap(self):
        """
        Sniffs packets to find beacon packets from access points
        """
        pkts = sniff(iface=self.iface, timeout=self.timeout)
        tcp, udp, icmp, other = str(pkts).replace('>', '').split()[1:]
        self.parse_metrics(tcp.split(':')[1], udp.split(':')[1],\
                                icmp.split(':')[1], other.split(':')[1])

    def run(self):
        """
        Runs the daemon and controls execution
        """
        try:
            while True:
                self.find_ap()
        except Exception as e:
            f = open('/var/log/panoptes/system.log', 'a+')
            f.write(f'Ap_metrics has encountered a problem {e}\n')
            f.close()

if __name__ == '__main__':
    pktstats = Packet_Stats('/tmp/packetStats.pid')
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1].lower():
            print('Starting')
            pktstats.start()
        elif 'restart' == sys.argv[1].lower():
            print('Restarted')
            pktstats.restart()
        elif 'stop' == sys.argv[1].lower():
            pktstats.stop()
            print('Stopped')
        else:
            print('Command Unknown')
            sys.exit(2)
    else:
        print(f'Usage: {sys.argv[0]} start|stop|restart')
        sys.exit(2)
