#!/usr/bin/env python3.6

import atexit
import os
import signal
import sys
import time

class Daemon:
    '''
        Daemon class to be subclasses by all other daemons
        Based on Sanser Marechal\'s \"Simple linux daemon in python2\"
    '''
    def __init__(self, pidf):
        self.pidfile = pidf

    def daemonise(self):
        ''' 
            Fork twice to stop zombie processes 
            Stackoverflow 881388
        '''
        try:
            pid = os.fork()
            if pid > 0:
                # close parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(f'Fork One Failed {e}')
            sys.exit(1)

        # decouple from parent evironment
        os.chdir('/') 
        os.setsid() 
        os.umask(0) # files that it creates permisions

        # second fork
        try:
            pid = os.fork()
            if pid > 0:
                # close second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(f'Fork Two Failed {e}')
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open('/var/log/panoptes/system.log', 'a+')
        se = open('/var/log/panoptes/system.log', 'a+')
        
        # Duplicate stdout files (org, dup)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write(f'{pid}|n')

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')
            f.close()

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        # Start
        # Open the pid file and if something in there then already running
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
                pf.close()
        except IOError:
            pid = None

        if pid:
            sys.stderr.write(f'pidfile {self.pidfile} already exists.' + \
                                'Daemon already running?\n')
            sys.exit(1)

        # "real" start
        self.daemonise()
        self.run()

    def stop(self):
        try:
            with open(self.pidfile, 'r') as pf:
                pid = pf.read().strip()
                # Needs investigation for some reason
                # somtimes pid = ''
                if pid:
                    pid = int(pid)
                pf.close()
        except IOError:
            pid = None

        if not pid:
            sys.stderr.write(f'pidfile {self.pidfile} does not exist.' + \
                                        ' Daemon not running?\n')
            return # won't be an error in restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as e:
            err = str(e.args)
            if str(e).find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)
    
    def restart(self):
        self.stop()
        self.start()

    def run(self):
        # Overide
        return
