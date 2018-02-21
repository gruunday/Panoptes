#!/usr/bin/env python3.6

import os
import imp
import sys
import subprocess
import argparse


def lst_plugins(directory='plugins'):
    """
    Lists plugins in a directory to be imported and ran

    :directory: name of directory to be imported
    """
    for fi in os.listdir(directory):
        if fi.startswith('_'):
            continue
        if not fi.endswith('.py'):
            continue
        path = os.path.join(directory, fi)
        yield imp.load_source(fi, path)

def run(cmd):
    """
    Run will run all the daemons in the directory yielded by lst_plugins

    :cmd: command to be given to the daemon
    """
    for plugin in lst_plugins():
        return_val = plugin.command(cmd)
        print(f'{str(plugin).split()[1]} ' + return_val)

def main():
    parser=argparse.ArgumentParser(
        description="""Panoptes, wireless monitoring solution""",
        epilog="""Panoptes, wireless monitoring solution""")
    parser.add_argument('start', nargs='*', default=[1, 2, 3], help='Starts all daemons in plugins folder')
    parser.add_argument('restart', nargs='*', default=[1, 2, 3], help='Restart all daemon in plugins folder')
    parser.add_argument('stop', nargs='*', default=[1, 2, 3], help='Stop all daemons in plugins folder')
    args=parser.parse_args()

    # Check script run with admin rights
    if os.getuid() != 0:
        print('This script needs root, please run with sudo')
        sys.exit(1)

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
    
    # Check args
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run('start')

if __name__ == '__main__':
    main()
