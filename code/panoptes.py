#!/usr/bin/env python3.6

import os
import imp
import sys

def lst_plugins(directory='plugins'):
    for fi in os.listdir(directory):
        if fi.startswith('_'):
            continue
        if not fi.endswith('.py'):
            continue
        path = os.path.join(directory, fi)
        yield imp.load_source(fi, path)

def run(cmd):
    for plugin in lst_plugins():
        return_val = plugin.command(cmd)
        print(f'{str(plugin).split()[1]} ' + return_val)

def main():
    # Check script run with admin rights
    if os.getuid() != 0:
        print('This script needs root, please run with sudo')
        sys.exit(1)

    # Check wifi card is in monitor mode
    ## TODO check if already in monitor mode
    ## TODO check if there is more than one card
    #try:
    #    os.system('ifconfig wlan1 down')
    #    os.system('iwconfig wlan1 mode monitor')
    #except:
    #    print('Can\'t change wireless card to monitor mode')
    
    # Check args
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run('start')

if __name__ == '__main__':
    main()
