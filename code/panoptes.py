#!/usr/bin/env python3.6

import os
import imp

#def load_plugins(self):
#    self.plugins = []
#    for plug in self.list_plugins():
#        self.plugins.append(plug)
#        f, filename, description = imp.find_module(plug, ['plugins'])
#        imp.find_module('ssid_detection', ['plugins'])
#        imp.load_module(plug, f, filename, description)

def lst_plugins(directory='plugins'):
    for fi in os.listdir(directory):
        if not fi.endswith(".py"):
            continue
        path = os.path.join(directory, fi)
        yield imp.load_source(fi, path)

def run():
    for plugin in lst_plugins():
        print(plugin)
        plugin.command('start')

if __name__ == '__main__':
    run()
