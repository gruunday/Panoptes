# !/usr/bin/env python3.6

import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
from alert import *
from scapy.all import *
import subprocess
from os import path
import json

class Ssid_Detection(Daemon):
    '''
        Class to detect a reservered ssid comming from an unkown mac address
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
        self.known_ssids = {}
        config = self.read_config()
        self.iface = config["ssid_detection"]["interface"]
        self.errorlog = config["ssid_detection"]["errorlog"]
        self.ssid_file = config["ssid_detection"]["known_ssids"]
        self.sleeptime = config["ssid_detection"]["sleeptime"]

    def read_config(self):
        """
        Reads in json config and sets configurable variables
        """
        basepath = path.dirname(__file__)
        config_path = path.abspath(path.join(basepath, "..", "config.json"))
        with open(config_path) as json_config:
            return json.load(json_config)

    # Is packet from an access pints
    def is_ap(self, pkt):
        """
        Checks if a packet is from an access point

        :pkt: Packet sniffed by scapy
        """
        if pkt.haslayer(Dot11ProbeResp) or pkt.haslayer(Dot11Beacon):
            ssid = pkt[Dot11Elt].info.decode('utf-8')
            mac = pkt[Dot11].addr3
            if (ssid in self.known_ssids) and (mac not in self.known_ssids[ssid]):
                self.send_alert(f'{ssid} was found with unknown mac {mac}')
    
    # Sniff packets in monitor mdoe
    def find_ap(self):
        """
        Sniffs packets to find beacon packets from access points
        """
        pkt = sniff(iface=self.iface,prn=self.is_ap)

    # Reads in config file
    def read_ssid(self):
        """
        Reads in all known ssids from config

        :raises FileNotFoundError: The config file could not be read/found
        """
        try:
            f = open(self.ssid_file, 'r')
        except FileNotFoundError:
            f = open(self.errorlog, 'a+')
            f.write('Error! Could not open /etc/known_ssid.txt')
            f.close()
            sys.exit(2)
        known_ssids = {}
        for line in f.readlines():
            line = line.split(';')
            ssid = line[0].replace(' ','')
            mac_list = line[1:]
            # Sanatise
            for i in range(len(mac_list)):
                mac_list[i] = mac_list[i].replace(' ','').replace('\n','')
            known_ssids[ssid] = mac_list
        self.known_ssids = known_ssids

    def send_alert(self, message):
        """
        Send a slack alert to channel

        :message: String message to send as alert
        """
        send_alert(message)

    def run(self):
        """
        Runs the daemon and controls execution
        """
        self.known_ssids = self.read_ssids() # ADD read in config name
        while True:
            self.read_ssid()
            self.find_ap()

if __name__ == '__main__':
    spoof = Ssid_Detection('/tmp/ssidDetection.pid')
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1].lower():
            print('Starting')
            spoof.start()
        elif 'restart' == sys.argv[1].lower():
            print('Restarted')
            spoof.restart()
        elif 'stop' == sys.argv[1].lower():
            spoof.stop()
            print('Stopped')
        else:
            print('Command Unknown')
            sys.exit(2)
    else:
        print(f'Usage: {sys.argv[0]} start|stop|restart')
        sys.exit(2)
