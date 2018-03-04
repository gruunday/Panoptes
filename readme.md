# Distributed Wifi Monitoring (aka Panoptes)

[![pipeline status](https://gitlab.computing.dcu.ie/doylet9/2018-CA326-tdoyle-distributedwifimonitoring/badges/master/pipeline.svg)](https://gitlab.computing.dcu.ie/doylet9/2018-CA326-tdoyle-distributedwifimonitoring/commits/master) [![coverage report](https://gitlab.computing.dcu.ie/doylet9/2018-CA326-tdoyle-distributedwifimonitoring/badges/master/coverage.svg)](https://gitlab.computing.dcu.ie/doylet9/2018-CA326-tdoyle-distributedwifimonitoring/commits/master)

## Project to collect and graph critical information about a wifi network.

## Team members

* Thomas Doyle
* Shanan Lynch

### Dependencies

* Python **3.6** or higher
* Pip3 for repository

### How to install

```
$ git clone https://gitlab.computing.dcu.ie/doylet9/2018-CA326-tdoyle-distributedwifimonitoring.git
$ cd 2018-CA326-tdoyle-distributedwifimonitoring/code/
$ chmod +x install.sh
$ ./install.sh
```

### How to use

* Once installed all the plugins will run on reboot. 
* If you do not want to reboot you can run them manualy by running the following options

> * [X] To start daemons call ```$ ./panoptes.py ``` *OR* ```$ ./panoptes.py start ```
> * [X] To stop daemons call ```$ ./panoptes.py stop```
> * [X] To restart daemons call ```$ ./panoptes.py restart```

### Configuration

#### Example Config

```json
{
    "slack": {
        "slack_token": "SLACK-API-KEY",
        "slack_channel": "#random",
        "slack_emoji": ":robot_face:",
        "slack_username": "Panoptes Alerts"},
    "ap_metrics":{
        "sleeptime" : 1,
        "interface" : "mon1",
        "pktcount" : 500},
    "nodeup" : {
        "sleeptime" : 5},
    "system_stats" : {
        "errorlog" : "/var/log/panoptes/system.log",
        "sleeptime" : 5},
    "ssid_detection" : {
        "interface": "mon1",
        "errorlog" : "/var/log/panoptes/system.log",
        "known_ssids" : "/etc/panoptes/known_ssids.txt"}
    "ping_metrics" : {
        "sleeptime" : 2},
    "packet_stats" : {
        "timeout" : 1,
        "interface": "mon1"}
}
```

* **sleeptime**: Refers to how often the pluings are run (seconds)
* **errorlog**: Refers to where logs are written for errors
* **slack_token**: Is the api key given to access your slack channel
* **interface**: Refers to what interface will be in monitor mode

### Plugins created

* [X] Ssid detection        - Detects ssids spoofing trusted ones
* [X] Metric fling          - Exports metrics to graphite database
* [X] Access Point Metrics  - Collects signal from surrounding access points
* [X] System Load Average   - Collects load average for nodes
* [X] Nodes Up              - Reports if a node is up
* [X] Ping Metrics          - Reports latency metrics
