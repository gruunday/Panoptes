#!/usr/bin/env python3.6
import sys
sys.path.append('/'.join(sys.path[0].split('/')[0:-1]))
from daemon import Daemon
from metric_fling import Metric_Fling
from alert import *
from scapy.all import *
import subprocess
from os import path
import time
import json

class Dhcp_Rogue_Det(Daemon):
    
    def __init__(self,pidf):
        Daemon.__init__(self,pidf)
        config = self.read_config()
        self.iface = config["dhcp_rogue_server"]["interface"]
        self.sleeptime = config["dhcp_rogue_server"]["sleeptime"]


    def read_config(self):
        """
        Reads in json config and sets configurable variables
        """
        basepath = path.dirname(__file__)
        config_path = path.abspath(path.join(basepath, "..", "config.json"))
        with open(config_path) as json_config:
            return json.load(json_config)

	# Reads in config file

    def check_dhcp_rogue_server(self):

        conf.checkIPaddr = False
        fam,hw = get_if_raw_hwaddr(self.iface)

        d_pkts = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=hw/DHCP(options=[("message-type","discover"),"end"]))

        ans, unans = srp(d_pkts, multi=True, timeout=3)

        srvs=[]

        for r in ans:
            print('DHCP offer from ' + result[1][IP].src + ' with MAC address ' + result[1][Ether].src)
            srvs.append(result[1][IP].src)

        if len(srvs) > 1:
            self.send_alert('WARNING possibiblity of DHCP Rogue Server')

        elif len(srvs) < 1:
            self.send_alert('No reply. Is there a DHCP server here????')

        else:
            self.send_alert('1 server detected. This is good')

        conf.checkIPaddr = True


    def send_alert(self, message):
        """
        Send a slack alert to channel

        :message: String message to send as alert
        """
        send_alert(message)

    def run(self):
        """
        Runs the daemon and controls execution
        """
        while True:
            self.check_dhcp_rogue_server()
            time.sleep(self.sleeptime)


if __name__ == '__main__':
	rogue = Dhcp_Rogue_Det('/tmp/dhcpR4.pid')
	if len(sys.argv) >= 2:
		if 'start' == sys.argv[1].lower():
		    print('Starting')
		    rogue.start()
		elif 'restart' == sys.argv[1].lower():
		    print('Restarted')
		    rogue.restart()
		elif 'stop' == sys.argv[1].lower():
			rogue.stop()
			print('Stopped')
		else:
		    print('Command Unknown')
		    sys.exit(2)
	else:
		print(f'Usage: {sys.argv[0]} start|stop|restart')
		sys.exit(2)

