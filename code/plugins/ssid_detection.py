# !/usr/bin/env python3.6

import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
from alert import slack_alert
from scapy.all import *
import subprocess

class Ssid_Detection(Daemon):
    '''
        Class to detect a reservered ssid comming from an unkown mac address
    '''
    def __init__(self, pidf):
        Daemon.__init__(self, pidf)
        self.known_ssids = {}

#    # Scans for ssids nearby
#    def find_ssids(self):
#        results = subprocess.check_output(["iwlist", "wlan1", "scan"])
#        results = results.decode("ascii").split("Cell")
#        found_ssids = {}
#        ssid = ''
#        mac = ''
#        for apoint in results:
#            output = ''
#            apoint = apoint.replace(' ', '').split('\n')
#            for entry in apoint:
#                if "Address" in entry:
#                    mac = entry.split(':', 1)[1]
#                elif "ESSID" in entry:
#                    ssid = entry.split(':')[1].replace('\"','')
#            if ssid in found_ssids:
#                found_ssids[ssid].append(mac)
#            elif ssid != '':
#                found_ssids[ssid] = [mac]
#        return found_ssids

    def is_ap(self, pkt):
        if pkt.haslayer(Dot11ProbeResp) or pkt.haslayer(Dot11Beacon):
            ssid = pkt[Dot11Elt].info.decode('utf-8')
            mac = pkt[Dot11].addr3
            f = open('/var/log/isitworking.txt', 'a+')
            f.write(ssid + mac + '\n')
            f.close()
            if (ssid in self.known_ssids) and (mac not in self.known_ssids[ssid]):
                self.send_alert(f'{ssid} was found with unknown mac {mac}')

    def find_ap(self):
        pkt = sniff(iface='mon1',count=10000,prn=self.is_ap)

    # Reads in config file
    def read_config(self):
        try:
            f = open('/etc/panoptes/known_ssids.txt', 'r')
        except FileNotFoundError:
            f = open('/var/log/panoptes/system.log', 'a+')
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

    # Checks ssids to see if they are reserved ones
#    def check_ssids(self, found_ssids, known_ssids):
#        for ssid in found_ssids:
#            if len(ssid) > 0 and ssid[0] == '\"':
#                ssid = ssid[1:-2]
#            if ssid in known_ssids:
#                known_macs = known_ssids[ssid]
#                if found_ssids[ssid] not in known_macs:
#                    self.send_alert(f'MAC Address {found_ssids[ssid]} ' +
#                            f'is not known for reserved SSID {ssid}')
    
    def send_alert(self, message):
        slack_alert(message)

    def run(self):
        self.known_ssids = self.read_config() # ADD read in config name
        while True:
            self.read_config()
            self.find_ap()
            #self.check_ssids(ssids, self.known_ssids)
            time.sleep(10)

def command(order):
    spoof = Ssid_Detection('/tmp/ssidDetection.pid')
    if 'start' == order:
        return 'Starting'
        spoof.start()
    elif 'restart' == order:
        return 'Restarted'
        spoof.restart()
    elif 'stop' == order:
        spoof.stop()
        return 'Stopped'
    else:
        return 'Command Unknown'
        sys.exit(2)

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
