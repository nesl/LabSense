LabSense
========

This project involves creating a sensing platform that can measure many
different characteristics about a lab (i.e. ambient temperature, 
electricity, water, occupancy). The project also focuses on making the data 
available with a user-intuitive interface.

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
code that receives notifications from the Homeseer Multisensor, the Aeon 
Labs Door/Window Sensor, and the Aeon Labs SmartSwitch. 

Zeromq is used as a transport layer to send the data from the 
LabSenseZwave executable to a python process that sends the data to SensorSafe.
This is meant to decouple the Zwave data retrieval from the possible slower
Http requests and network latency. 

Dependency:

* [Open-zwave](http://code.google.com/p/open-zwave/)
* [Zeromq](http://www.zeromq.org/intro:get-the-software)

------------------------------------------------------------------------------

Hardware Requirements
---------------------
This software is running on a [Guruplug Server](http://www.globalscaletechnologies.com/t-guruplugdetails.aspx) with an
[Aeon Labs Z-stick](http://www.aeon-labs.com/site/products/view/2/). 
The sensors that interact with the Z-stick include:

* [Aeon Labs Door/Window Sensor](http://www.aeon-labs.com/site/products/view/1/)
* [Homeseer MultiSensor](http://store.homeseer.com/store/HomeSeer-HSM100-S2-Z-Wave-Multi-Sensor-P1189C57.aspx)
* [Aeon Labs SmartSwitch](http://www.aeon-labs.com/site/products/view/5/)

------------------------------------------------------------------------------

Installation
--------------
1. Install needed development headers for open-zwave:

    sudo apt-get install libudev-dev

2. Install Zeromq by following directions at http://www.zeromq.org/intro:get-the-software
3. Install python bindings by following directions at http://www.zeromq.org/bindings:python
4. Get the open-zwave source code using svn by running:

    svn checkout http://open-zwave.googlecode.com/svn/trunk/ open-zwave/

5. Navigate to open-zwave/cpp/examples/linux/
6. Get the source code for this project using git or download it:

    git clone git@github.com:jtsao22/LabSense.git

   The LabSense Project should now be at open-zwave/cpp/examples/linux/LabSense.

7. Navigate to LabSense/LabSenseZwave/
8. Make the code and run the executable

    make 
    ./LabSenseZwave [serial port]

   To figure out what serial port, please plug the Z-stick into the Guruplug and run dmesg. A line similar to the following should specify the port:

   "cp210x converter now attached to [serial port]"

   Unless other usb devices are plugged in, usually the serial port is /dev/ttyUSB0. 

The previous steps are used for local viewing of the data coming off the sensors. If an online graphical view of the
sensor data is required, more code has been implemented to send the data to [SensorSafe](https://128.97.93.29/):

1. Register for a SensorSafe account and take note of the API key.
2. The python script sendToSensorSafe.py sends the data it receives over the zeromq socket to SensorSafe, which requires
an API key. Create a file in the same directory as sendToSensorSafe.py called api_key.py and write a single line:

    key = "[SensorSafe API Key]"

    where SensorSafe API Key is given to you after registering for SensorSafe.
3. Finally, to send the data to SensorSafe, run the python script sendToSensorSafe.py while running the LabSenseZwave
executable:

    python sendToSensorSafe.py

    (Either run this in a separate ssh session/terminal or run one of the processes in the background).
4. The script will send to SensorSafe as soon as all variables have been initialized (temperature, luminance, and
motion_timeout), which make take some time depending on the wake-up interval of the Homeseer Multisensor (programmed to
be every 6 minutes).
Upon successful upload to SensorSafe, a message similar to the following will show up:

    200 OK
    [('transfer-encoding', 'chunked'), ('vary', 'Accept-Encoding'), ('server', 'Apache/2.2.11 (Ubuntu) mod_ssl/2.2.11
    OpenSSL/0.9.8g mod_wsgi/2.3 Python/2.6.2'), ('connection', 'close'), ('date', 'Tue, 10 Apr 2012 19:47:03 GMT'),
    ('access-control-allow-origin', '*'), ('content-type', 'text/html; charset=utf-8')]
    Upload successful (Collection name: sandbox, Requested by sandbox
5. You can then see the data on SensorSafe by signing in, pressing access data, selecting data channels, and pressing Show Data. 

------------------------------------------------------------------------------

By Jason Tsao
