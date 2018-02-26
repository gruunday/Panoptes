# Panoptes Technical Manual

## 0. Contents

   1. Introduction
       1.1 Overview
       1.2 Glossary
   2. System Architecture
   3. High-Level Design
   4. Problems and Resolution
   5. Installation Guide

## 1. Introduction

#### 1.1 Overview

> This project is setting out to be able to monitor wifi networks across and organisation, from small scale like a coffee shop, to large scale in a college campus. We want the nodes to be relitivly cheap and also work well on a large, distributed scale. 
> A lot of attacks can be performed on wifi networks and we hope to add intrustion detection in our system to alert to such attacks. We also want to collect statistics on the wifi network to alert administrators of the network to poor performance, outages and black spots. 

#### 1.2 Glossary

* Kali Linux : Linux with prebuilt tools for low level networking and penetration testing.
* Raspberry pi: Small form factor and reasonably priced computer that provides stealth and portability of the system 

## 2. System Architecture

> The system will run on raspberry pis, cheap and small form factor computers. They have a wireless card build in but this is not capable of monitor mode. 
> We also need an interface in managed mode to pass metrics about the device back to the server. For this reason we are using a Alfa networking card with a Ralink Technology, Corp. RT2870/RT3070 chipset and the driver on that chip at the time of development is rt2800usb. For outages and doggy wifi zones the ethernet port on the raspberry pi can be used and will failover in the event of wifi going down. This can also be configured as the primary way to send metrics. 
> Because what we are doing is detering hackers, we must employ the use of tools the hackers use. So we are using a linux distrbution for the raspberry pi operating system called kali (previously known as backtrack). 

#### 2.1 Language Choice

> Python is a very easy to read language with many nice features including the scapy library
> Python 2 is being depricated in 2020 so we felt this was not an option, even though it has a better track record with working with byte strings 
> Python 3.6 has new features such as f-strings that would clean up our code, it has much improved on it's handling of byte strings and it has over come it's speed problem to pass out python 2.7 in speed. 
> For the reasons mentioned above pyton 3.6.4 was the winner and what was decided to develop the project in.
> This is by far the ideal language and run time is affected by this choice. But when we look at the timeframe of the project we would not have the features we have today in as little a time with any other language.

## 3. High-Level Design

## 4. Problems and Resolution

> Metrics when sent with UDP to graphite do not show up in graphite but they do with TCP. This is still to be investigated further but the resoution is to use tcp for sending metrics. To optimise this workaround we plan to send metrics as a batch pickeled to avoid congesting wifi traffic with the monitoring system.

> When testing metric fling we are trying to send a metric and also catch that metric going across the wire to the server. To do this we have had to create a work around where a thread sends metric on a loop and scapy will sniff and stop on the first one that matches a filter of what that metric should look like. More checks are then done on that packet, i.e. destination port. While this testing method is not ideal we are confident it the capablility of it catching most errors

> While attempting to test the restart method for daemons the daemon will fork away from unittest causing errors. It is not known how this will be tested or it will be a redesign of how the restart method is implemented but it is a known defect.

> While trying to have automatic deployment from our repo (i.e every time there is a merge to master and tests pass we deploy to all raspberry pis) we found difficulty doing this. For one the raspberry pis do not have static ips. This means that we do not know, or want hard coded in what each of their addresses are to send the updates. This means we have to come to a compramise. We will have the pi's go to the repo an d fetch it every few minutes, configurable in the config. This does not come without it's own set of problems though, one of such is each pi will need authorised ssh keys to the repo. There may be a better solution to this again, but we have a lot of issues and this solution will work for the temporary future.

## 5. Installation Guide

> Insert readme.md before submition 
