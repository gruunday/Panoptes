# !/usr/bin/env python3.6

import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from scapy.all import *
from daemon import Daemon
from metric_fling import Metric_Fling
import platform
import time
import json

class Ap_Metrics(Daemon):
    '''
        Class to collect metrics on access points
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
        self.metric = Metric_Fling()
        self.data = []
        config = self.read_config()
        self.sleeptime = config["ap_metrics"]["sleeptime"]
        self.iface = config["ap_metrics"]["interface"]
        self.pktcount = config["ap_metrics"]["pktcount"]

    def read_config(self):
        """
        Reads in json config files and sets configurable variables
        """
        with open('config.json') as json_config:
            return json.load(json_config)

    # Is packet from an access pints
    def is_ap(self, pkt):
        """
        Checks to see if a packet came from an access point

        :pkt: Packet sniffed by scapy
        """
        if pkt.haslayer(Dot11ProbeResp) or pkt.haslayer(Dot11Beacon):
            ssid = pkt[Dot11Elt].info.decode('utf-8')
            mac = pkt[Dot11].addr3
            signal = int(pkt[RadioTap].dbm_antsignal)
            path = f'{platform.node()}.accesspoint.metric.signal'
            # Export as both to do queries based on both 
            self.data.append(f'\n{path}.{mac} {signal} {time.time()}\n')
            self.data.append(f'\n{path}.{ssid}.{mac} {signal} {time.time()}\n')
            # Ensure that metrics **START AND END** with new lines
            # It will ##NOT## work without it
            
    # Sniff packets needs monitor mode, set in panoptes
    def find_ap(self):
        """
        Sniff packets comming in to find access point broadcast packets
        """
        pkt = sniff(iface=self.iface,count=self.pktcount,prn=self.is_ap)

    def run(self):
        """
        Runs command and controls execution
        """
        while True:
            self.find_ap()
            self.metric.tcp_fling(self.data)
            self.data = []
            time.sleep(self.sleeptime)

# How panoptes controls daemon
def command(order):
    """
    Recieves command from panoptes to start stop or restart

    :order: string command to decide what to do
    """
    metric = Ap_Metrics('/tmp/apMetrics.pid')
    if 'start' == order:
        return 'Starting'
        metric.start()
    elif 'restart' == order:
        return 'Restarted'
        metric.restart()
    elif 'stop' == order:
        metric.stop()
        return 'Stopped'
    else:
        return 'Command Unknown'
        sys.exit(2)

if __name__ == '__main__':
    metric = Ap_Metrics('/tmp/apMetrics.pid')
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1].lower():
            print('Starting')
            metric.start()
        elif 'restart' == sys.argv[1].lower():
            print('Restarted')
            metric.restart()
        elif 'stop' == sys.argv[1].lower():
            metric.stop()
            print('Stopped')
        else:
            print('Command Unknown')
            sys.exit(2)
    else:
        print(f'Usage: {sys.argv[0]} start|stop|restart')
        sys.exit(2)
