# Functional Specification

## Table of contents

1. [Introduction](##Introduction)
    1.1 [Overview](###Overview)
    1.2 [Glossary](###Glossary) 
2. [General Description](##General\ Description)
    2.1 [Product / System Functionalities](###Product\ \/\ System\ Functionalities)
    2.2 [User Characteristics and Objectives](User\ Characteristics\ and\ Objectives)
    2.3 [Operational Scenarios](###Operational\ Scenarios)
    2.4 [Constraints](###Constraints)
3. [Functional Requirements](##Functional\ Requirements)
4. [System Architecture](##System\ Architecture)
5. [High-Level Design](##High-Level\ Design)
6. [Preliminary Schedule](##Preliminary\ Schedule)
7. [Appendices](##Appendices)

## Introduction

### Overview:

The product we are developing is a product to make it easier for admins to detect malicious activity and wifi performance throughout the system. We are doing this by placing raspberry pis or nodes strategically around the campus, business or organization. The Raspberry Pis will be running kali linux which is a distribution specifically for network penetration and testing. On Kali linux we are using scapy with python to run scripts to sniff packets and create packets to test our snort rules. The scripts will be collecting and logging critical information about the wireless network to be received by the server where they will be graphed and processed. Snort is a network intrusion detection system (NIDS) that will be used as a filter for the packets. We will be filtering the packets by creating rules for what we want to filter and detect. Snort can be used to send alerts when the filters catch unusual traffic which does not match the usual network activity. With all of the information collected from the python scripts and snort, we will be displaying the information using graphite and grafana. This will display and accurate representation of the state of their system to the client/admin on the other end. This will also have the ability to display historical statistics providing that the system was running and listening at the time.


### Glossary:

* **Kali Linux**: 
    * Linux distribution targeted towards offensive security and penetration testing
* **Raspberry Pis**: 
    * Small cheap computers with bluetooth and wifi built in
* **Grafana**: 
    * Web front or displaying graphs and querying metrics from graphite
* **Graphite**: 
    * Backend for Grafana collects data and metrics. 
* **NIDS**: 
    * Network intrusion detection system looks at packets on the network and will detect and alert known patterns in these packets as malicious activity
* **CLI**: 
    * Command Line Interface

## General Description

### Product / System Functions:

The function of this product is to be able to detect malicious activity while, also, accurately displaying information and metrics related to the wireless network to the admin or client. This information will include details of any ongoing problems with the Wifi signal throughout the organisation, and also screening for any abnormalities and malware on the network.


### User Characteristics and Objectives:

We expect our users to be very well adapted to technology, as we expect that most of our user base will be admins. From the user's perspective the software should detect and give alerts of malicious or unusual activity within the network with minimal configuration needed day to day. Most of the interaction will be querying and browsing graphs through grafana and graphite or querying a command line interface(CLI)


### Operational Scenarios:

#### User Mike Logs onto grafana

* Current System State: Server is collecting metrics and graphite collecting
* Informal Scenario: User Mike enters the username and password and is granted access to all the statistics being collected by the system.
* Next Scenario: User Mike wants to make new graph

* User Mike Logs wants to make a new graph
* Current System State: User Mike is logged in
* Informal Scenario: User Mike adds a new panel and creates graphite query
* Next Scenario: User Mike creates an alert for the newly created graph

* User Mike makes an alert
* Current System State: User Mike has made a graph
* Informal Scenario: User Mike clicks on the alert tab and enters the value at which he wants an alert to go to him and how he wants that alert be received
* Next Scenario: User Mike wants to make new alert to detect ARP poisoning

* User Mike checks for ARP poisoning
* Current System State: User Mike is logged in and has made graphs
* Informal Scenario: User Mike queries the graphite database to see if there are any devices that are suspected to be performing ARP poisoning and sets up an alert in the alert tab.
* Next Scenario: User Mike hears a report the wifi has been bad in an area 

* User Mike checks wifi in an area
* Current System State: Mike is logged on
* Informal Scenario: Mike finds the node in that area and looks at the graph. He sees that the connection to the access point does not drop but there are too many packets for the access point to handle causing a bottleneck.
* Next Scenario: Mike wants to view the throughput of an access point

* Mike wants to check throughput of access point
* Current System State: Mike is logged on
* Informal Scenario: Mike goes to the node that is near the access point. He queries the graphite database to see what the throughput is throughout the day
* Next Scenario: Mike wants to find what node can see an access point with a known mac address

* Mike wants to know who can see a certain access point
* Current System State: Mike logs onto the CLI
* Informal Scenario: Mike queries the system with the mac address of the access point and it return what node(s) can see it
* Next Scenario: Mike logs onto grafana

## Functional Requirements

### Node Automatic Connection To Server

* Description - The node once deployed and turned on with a fully configured system should be able to look and find the server automatically, and headlessly
* Criticality - This is most critical. Without connecting to server we have no way to collect metrics
* Technical issues - Figuring out how allow a node to automatically find the server
* Dependencies with other requirements - None

### Network Metric Collection

* Description - The system should collect metrics about wireless networks around it.
* Criticality - This is most critical. Everything relies on this.
* Technical issues - Figuring out how to collect these metrics fast and reliably
* Dependencies with other requirements - None

### Network Reliability Collection

* Description - The system should collect metrics about how reliable the system has been in previous history
* Criticality - This is critical. We want to see at what time the network is failing and how often
* Technical issues - Figuring out how to collect these metrics fast and reliably and on a possibly failing wifi network
* Dependencies with other requirements - None

### Alert System

* Description - The system needs to be able to alert to errors, and malicious activity
* Criticality - This is critical. Without this, many abnormalities may go unseen to admins
* Technical issues - Figuring out what to page for and what to log for. Also are there different ways to alert, emails for less important, slack message for urgent
* Dependencies with other requirements - Metrics being collected

### Local SSID Collection
* Description - The system should log all ssids that is sees and check that there mac address is known
* Criticality - This is critical. This needs to be alerted to
* Technical issues - Figuring out how to collect these metrics fast and reliably
* Dependencies with other requirements - Depends on network to be functional

### Network DCHP Server Collection
* Description - The system should collect metrics about all DCHP servers and ensure that they are belonging to the organisation and not a spoof
* Criticality - This is critical. This needs to be alerted to
* Technical issues - Figuring out how to collect these metrics fast and reliably
* Dependencies with other requirements - Depends on alerts to be operational

### Node Up Check
* Description - We need to monitor what nodes are up and what nodes have gone down
* Criticality - This is important. This is crutical to detecting broken areas of a network
* Technical issues - Figuring out how to create our own tcp ping packet, that will let the server and the node know that they have lost communication
* Dependencies with other requirements - None

### Network Speed Metric Collection
* Description - The system should collect metrics about how fast the wireless network is, both download and upload
* Criticality - This is important. This is a significant metric
* Technical issues - Figuring out how to collect these metrics fast and reliably without causing stress to the network for users
* Dependencies with other requirements - None

### Wireless throughput Metric Collection
* Description - The system should collect metrics about much throughput we have on the wireless network
* Criticality - This is important, it is a significant metric
* Technical issues - Figuring out how to transfer file from server to node and measure throughput accurately
* Dependencies with other requirements - Connection to server

### Network Range Metric Collection
* Description - The system should collect metrics about how strong the wifi signal is from all the access points
* Criticality - This is important. This is a significant metric
* Technical issues - Figuring out how to collect these metrics fast and reliably
* Dependencies with other requirements - Depends on network to be functional

### Network Metric Retrieval
* Description - The server needs to be able to retrieve the information from it’s notes. Without this we can not see anything happening on the network.
* Criticality - Very Critical. 
* Technical issues - How to reliably send these metrics in real time across the network without too much loss of data.
* Dependencies with other requirements - Depends on the nodes collecting metrics

### Grafana Receiving Metrics
* Description - Grafana needs to be receiving metrics from Graphite in order to display the data. 
* Criticality - Moderately Critical, graphite can display graphs in an ugly manner
* Technical issues - Metric hand over needs to be fast to show real time information
* Dependencies with other requirements - Depends on Grafana

### Snort Rules
* Description - Snort needs to have rules that will filter malicious traffic
* Criticality - Moderately Critical, malicious activity will not be detected
* Technical issues - Testing snort rules with scapy and learning how to train snort rules for effective alerting rather than a false positive
* Dependencies with other requirements - Depends on scapy tests

### System handles loss of node, server connection
* Description - The node and system loose contact, the nodes decide to pass metrics to node with most free storage
* Criticality - This is a great feature, but difficult to implement
* Technical issues - Creating a fast algorithm to do graph search and reliably handing metrics over to an underpowered node. Ensuring that when the node storage fills up next node will take over but they should not end up in a loop of handing metrics back and forth.
* Dependencies with other requirements - Nodes collecting metrics

### Traceroute Debug
* Description - The server should have the ability to trace a connection to a node to find at what point to communication is broken through a cli.
* Criticality - Very useful. Would make debugging easier
* Technical issues - How to program our own traceroute feature
* Dependencies with other requirements - None

## Constraints

### Time constraints
* The project should be completed by the DCU 3rd year project deadline on Friday the 9/3/2018 at 5pm.

### Functional constraints
* The project should include all the functionality that this document describes, and it should be obvious that the functionality exists.

### User constraints
* The features should be easy to use or quick to learn for a user of substantial network knowledge, eg. system administrator and this project should include enough documentation to allow the user to get up to speed fast with how to use and install this tool with minimal headache.

## System Architecture

![Architechture Diagram](Architechture.png)

## High-Level Design

![High level design diagram](HighLevelDesign1.png)

## Preliminary Schedule

![Ghant chart](timetable.png)
