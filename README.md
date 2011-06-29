LabSense
========

This project involves creating a sensing plaform that can measure many
different characteristics about a lab (i.e. ambient temperature, 
electricity, water, occupancy) and making the data available in a user
intuitive interface.

LabSenseServer
--------------

LabSenseServer contains the code running on the server, which communicates
with a plug computer (Guru plug) that is present in every laboratory that
is equipped. Each guru plug talks to several different sensors through a
multitude of different protocols (i.e. Zigbee, Bluetooth, Zwave).

This server will also host a website through which users can view the
different sensor outputs in a intuitive interface. 

The server will also serve a public api that others can use to read the
data from the different sensors. Other applications can then process the
data and perform their own analysis of the streaming data.

Dependency:

* [Django 1.3.1](https://www.djangoproject.com/download/)

------------------------------------------------------------------------------

LabSenseZwave
--------------

LabSenseZwave contains the code running on the guruplug. This code 
specifically focuses on the zwave aspect of the guruplug. The open-zwave 
project is used for the zwave implementation. The Main.cpp file contains the
code that receives notifications from the HSM-100 and the Aeon Labs Door/
Window Sensor. Zeromq is used as a transport layer to send the data from the 
LabSenseZwave executable to a python process that sends the data to SensorSafe.
This is meant to decouple the Zwave data retrieval from the possible slower
Http requests and network latency. 

Dependency:

* [Open-zwave](http://code.google.com/p/open-zwave/)
* [Zeromq](http://www.zeromq.org/intro:get-the-software)

------------------------------------------------------------------------------
By Jason Tsao

