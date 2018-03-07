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

#### Installing the OS

First we need to download the kali linux image from [kali website](https://www.offensive-security.com/kali-linux-arm-images/#1493408272250-e17e9049-9ce8)

Or with the following command 

```bash
$ wget https://images.offensive-security.com/arm-images/kali-linux-2018.1a-rpi3-nexmon.img.xz
```

> **Remember** : Never download Kali Linux images from anywhere other than the official sources, and you should go [here](https://docs.kali.org/kali-on-arm/install-kali-linux-arm-raspberry-pi) to see how to verify your image 

Once we have our image we want to write it to and sd card. Insert the sd card into your machine and type

```bash
$ sudo fdisk -l
```

Find the disk that is your sd card (should be something like /dev/sdb, but may not) 

**Warning** Make sure this is not your harddrive and is your sd card, everything will be overwritten

When you have found your card you can write the image to the card with the following command

```bash
$ sudo dd if=PATH of=DEST bs=512k
```

where PATH will be the path to where you downloaded the fie to
and DEST will be the path to your sd card we found earlier, e.g. /dev/sdb

Now you can remove your sd card pop it in your pi and boot it up. We are gonna need a monitor keyboard and mouse for this next bit

#### Installing the Software on the OS

```bash
$ git clone https://gitlab.computing.dcu.ie/doylet9/2018-CA326-tdoyle-distributedwifimonitoring.git
$ cd 2018-CA326-tdoyle-distributedwifimonitoring/code/
$ chmod +x install.sh
$ ./install.sh
```

### How to use

* Once installed all the plugins will run on reboot. 
* If you do not want to reboot you can run them manualy by running the following options

```bash
./start # To start all the plugins

./stop  # To stop  all the plugins

./start && ./stop # To restart all the plugins
``` 

> If you do not like, want or need a plugin just move it to another folder

```bash
mkdir bakupPlugins
mv pluings/example bakupPlugins/example
```

### Configuration

You can change many things about the project so that is runs to suit your needs. The following is an example config you can use to get your started.

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
