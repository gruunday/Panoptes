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
    mode = subprocess.check_output(['iw', 'dev'])
    mode = mode.decode('utf-8').split('\n')[5].strip().split()[1]
    if mode != 'monitor':
        try:
            device = subprocess.check_output(['iw','dev'])
            device = device.decode('utf-8').split('\n')[0].replace('#','')
            os.system(f'iw phy {device} interface add mon1 type monitor')
            os.system('iw dev wlan1 del')
            os.system('ifconfig mon1 up')
            print('Wireless card in monitor mode')
        except:
            print('Can\'t change wireless card to monitor mode')

    if sys.argv[-1] == 'start':
        os.system(f'./start')
    elif sys.argv[-1] == 'restart':
        os.system(f'./stop')
        os.system(f'./start')
    elif sys.argv[-1] == 'stop':
        os.system(f'./stop')
    else:
        print('Unknown command')

if __name__ == '__main__':
    main()
