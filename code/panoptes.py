#!/usr/bin/env python3.6

import os
import imp

def lst_plugins(directory='plugins'):
    for fi in os.listdir(directory):
        if not fi.endswith(".py"):
            continue
        path = os.path.join(directory, fi)
        yield imp.load_source(fi, path)

def run():
    for plugin in lst_plugins():
        plugin.command('start')

if __name__ == '__main__':
    run()
