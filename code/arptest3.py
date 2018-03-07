#!/usr/bin/env python3.6
import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
from alert import *
from scapy.all import *
import subprocess
import netifaces
from os import path
import time
import json

class arp_Test(Daemon):
    '''
        Class to detect a reservered ssid comming from an unkown mac address
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
       
        config = self.read_config()
        self.count_mac = {}
        self.reqs = []
        self.net = netifaces.ifaddresses(self.iface)
        self.l_ip = net[netifaces.AF_INET][0]["addr"]
        self.b = net[netifaces.AF_INET][0]["broadcast"]
        self.iface = config["arp_Test"]["interface"]
        self.sleeptime = config["arp_Test"]["sleeptime"]
        self.mac_limit = config["arp_Test"]["maclimit"]


    def read_config(self):
        """
        Reads in json config and sets configurable variables
        """
        basepath = path.dirname(__file__)
        config_path = path.abspath(path.join(basepath, "..", "config.json"))
        with open(config_path) as json_config:
            return json.load(json_config)

    
    # Sniff packets in monitor mdoe
    def find_arp(self):
        """
        Sniffs packets to find arp requests
        """
        sniff(filter = "arp", prn = pkt_contents, store = 0)

    def clean(source, src_mac, dtn):
        if dtn == self.b:
            if not src_mac in self.count_mac:
                self.count_mac[src_mac] = 0

        if not source in self.reqs and source != self.l_ip:
            if not src_mac in self.count_mac:
                self.count_mac[src_mac] = 0
            else:
                self.count_mac[src_mac] += 1

            if self.count_mac[src_mac] > self.mac_Limit:
                send_alert(src_mac + " this machine is poisoning")

        else:
            if source in self.reqs:
                self.reqs.remove(source)               

    

    def pkt_contents(self, packet):
        source = packet.sprintf("%ARP.prsc%")
        dest = packet.sprintf("%ARP.pdst%")
        mac = packet.sprintf("%ARP.hwsrc%")
        if source == self.l_ip:
            self.reqs.append(dest)
        if packet.sprintf("%ARP.op%") == 'is-at':
            clean(source, mac, dest)
   

    def send_alert(self, message):
        """
        Send a slack alert to channel

        :message: String message to send as alert
        """
        pushbullet_aler(message)
        slack_alert(message)

    def run(self):
        """
        Runs the daemon and controls execution
        """
        while True:
            self.find_arp()
            time.sleep(self.sleeptime)


if __name__ == '__main__':
    poison = arp_Test('/tmp/arptest3.py')
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1].lower():
            print('Starting')
            poison.start()
        elif 'restart' == sys.argv[1].lower():
            print('Restarted')
            poison.restart()
        elif 'stop' == sys.argv[1].lower():
            poison.stop()
            print('Stopped')
        else:
            print('Command Unknown')
            sys.exit(2)
    else:
        print(f'Usage: {sys.argv[0]} start|stop|restart')
        sys.exit(2)

