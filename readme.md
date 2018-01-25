# Distributed Wifi Monitoring (aka Panoptes)

[![pipeline status](https://gitlab.computing.dcu.ie/doylet9/2018-CA326-tdoyle-distributedwifimonitoring/badges/master/pipeline.svg)](https://gitlab.computing.dcu.ie/doylet9/2018-CA326-tdoyle-distributedwifimonitoring/commits/master)

## Project to collect and graph critical information about a wifi network.

## Team members

* Thomas Doyle
* Shanan Lynch

### Dependencies

* Python **3.6** or higher

### How to install

```
$ git clone https://gitlab.computing.dcu.ie/doylet9/2018-CA326-tdoyle-distributedwifimonitoring.git
$ cd 2018-CA326-tdoyle-distributedwifimonitoring/code/
$ chmod +x install.sh
$ ./install.sh
```

### How to use

* [X] To start daemons call ```$ ./panoptes.py ``` *OR* ```$ ./panoptes.py start ```
* [X] To stop daemons call ```$ ./panoptes.py stop```
* [X] To restart daemons call ```$ ./panoptes.py restart```

### Plugins created

* [X] Ssid detection - Detects ssids spoofing trusted ones
* [X] Metric fling   - Exports metrics to graphite database
