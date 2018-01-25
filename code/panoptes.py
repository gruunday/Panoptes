#!/usr/bin/env python3.6

import os
import imp
import sys

def lst_plugins(directory='plugins'):
    for fi in os.listdir(directory):
        if not fi.endswith(".py"):
            continue
        path = os.path.join(directory, fi)
        yield imp.load_source(fi, path)

def run(cmd):
    for plugin in lst_plugins():
        print(plugin)
        return_val = plugin.command(cmd)
        if return_val == 'Starting':
            print(f'{plugin} OK...')
        else:
            print(f'{plugin} Not started...')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run('start')
