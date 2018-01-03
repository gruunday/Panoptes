# !/usr/bin/env python3.6

from daemon import Daemon
from metric_fling import Metric_Fling 
import subprocess

def find_ssids():
    results = subprocess.check_output(["iwlist", "wlan0", "scan"])
    results = results.decode("ascii").split("Cell")
    found_ssids = {}
    ssid = ''
    mac = ''
    for apoint in results:
        output = ''
        apoint = apoint.replace(' ', '').split('\n')
        for entry in apoint:
            if "Address" in entry:
                mac = entry.split(':', 1)[1]
            elif "ESSID" in entry:
                ssid = entry.split(':')[1].replace('\"','')
        if ssid in found_ssids:
            found_ssids[ssid].append(mac)
        elif ssid != '':
            found_ssids[ssid] = [mac]
    return found_ssids

def read_config():
    f = open('known_ssids.txt', 'r')
    known_ssids = {}
    for line in f.readlines():
        line = line.split(';')
        ssid = line[0].replace(' ','')
        mac_list = line[1:]
        # Sanatise
        for i in range(len(mac_list)):
            mac_list[i] = mac_list[i].replace(' ','').replace('\n','')
        known_ssids[ssid] = mac_list
    return known_ssids

def check_ssids(found_ssids, known_ssids):
    for ssid in found_ssids:
        if len(ssid) > 0 and ssid[0] == '\"':
            ssid = ssid[1:-2]
        if ssid in known_ssids:
            known_macs = known_ssids[ssid]
            if found_ssids[ssid] not in known_macs:
                alert(f'MAC Address {found_ssids[ssid]} ' +
                        f'is not known for reserved SSID {ssid}')

def alert(message):
    print('*' * (len(message) + 4))
    print(f'* {message} *')
    print('*' * (len(message) + 4))

def main():
    print('Loading config...')
    known_ssids = read_config() # ADD read in config name
    print('Starting...')
    while True:
        print('Finding ssids')
        ssids = find_ssids()
        print('Checking ssids')
        check_ssids(ssids, known_ssids)

if __name__ == '__main__':
    main()
