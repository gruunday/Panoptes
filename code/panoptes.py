#!/usr/bin/env python3.6

import os
import imp
import sys
import subprocess
import argparse

def main():
    parser=argparse.ArgumentParser(
        description="""Panoptes, wireless monitoring solution""",
        epilog="""Panoptes, wireless monitoring solution""")
    parser.add_argument('start', nargs='*', default=[1, 2, 3], help='Starts all daemons in plugins folder')
    parser.add_argument('restart', nargs='*', default=[1, 2, 3], help='Restart all daemon in plugins folder')
    parser.add_argument('stop', nargs='*', default=[1, 2, 3], help='Stop all daemons in plugins folder')
    args=parser.parse_args()

    # Check wifi card is in monitor mode
    ## TODO check if already in monitor mode
    ## TODO check if there is more than one card
    cards = subprocess.check_output(['airmon-ng'])
    cards = cards.decode('utf-8').split('\n')[3:-2]
    mon_device = None
    for device in cards:
        device = device.split('\t')
        if device[-1] == 'Ralink Technology, Corp. RT2870/RT3070':
            mon_device = device[1]
            mon_name = device[0]
    if mon_device == None:
        with open('/var/log/panoptes/system.log', 'a+') as f:
            f.write('Could not find an interface to monitor on in panotpes')
        sys.exit(9)
    try:
        os.system(f'iw phy {mon_name} interface add mon1 type monitor')
        os.system(f'iw dev {mon_device} del')
        os.system('ifconfig mon1 up')
        print('Wireless card in monitor mode')
    except Exception as e:
        print(f'Can\'t change wireless card to monitor mode {e}')

if __name__ == '__main__':
    main()
