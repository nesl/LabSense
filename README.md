LabSense
========

This project involves sensing many different characteristics about a lab (i.e.
ambient temperature, electricity, water, occupancy) and making the data
available in a user intuitive interface. There are several components to the
project and can function on their own. Each component is assigned to its own
directory. The components all communicate using zeromq. Each component sends
data to a python script (sendToSensorSafe.py), which parses all the data and
sends it to SensorSafe. SensorSafe is a platform for sharing sensory
information online that graphs data.

------------------------------------------------------------------------------
Components 
=========

LabSenseServer
--------------

LabSenseServer contains the code running on the server, which communicates
with a plug computer (Guru plug) that is present in every laboratory that
is equipped. Each guru plug talks to several different sensors through a
multitude of different protocols (i.e. Zigbee, Bluetooth, Zwave).

This server will also host a website through which users can view the
different sensor outputs in an intuitive interface. 

The server will also serve a public api that others can use to read the
data from the different sensors. Other applications can then process the
data and perform their own analysis of the streaming data.

Dependency:

* [Django 1.4](https://www.djangoproject.com/download/)

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

Dependencies:

* [Open-zwave](http://code.google.com/p/open-zwave/)
* [Zeromq](http://www.zeromq.org/intro:get-the-software)

------------------------------------------------------------------------------

LabSensePowerMonitor
--------------

LabSensePowerMonitor contains the code to read the data from the Veris E30A
Power Panel Monitor. The code is based on the Application Protocol for the Veris
E30 Panel-board Monitoring System, which is based on accessing memory-mapped
registers by issuing register-read or register-write request messages. The code
is based on code written by [Jaein Jong](http://local.cs.berkeley.edu/wiki/images/5/5c/Panel_monitoring_techrpt_jeong.pdf).
The LabSensePowerMonitor forwards power and current readings from the Vera E30
to the sendToSensorSafe.py file over Zeromq.

Dependencies:

* [Zeromq](http://www.zeromq.org/intro:get-the-software)

------------------------------------------------------------------------------

LabSenseRaritan
--------------

LabSenseRaritan contains the code to read the data from the [Raritan PX8](http://www.raritan.com/support/dominion-px/v1.3.5/user-guides/english/DPX-0L-v1.3.5-E.pdf),
a power distribution unit to monitor power on server racks. 

Dependencies:

* [Zeromq](http://www.zeromq.org/intro:get-the-software)
* [PySNMP](http://pysnmp.sourceforge.net/quickstart.html)

------------------------------------------------------------------------------

LabSenseForwarder
-----------------

LabSenseForwarder contains the code that receives all zeromq messages from all
of the components. This directory only contains one file: sendToSensorSafe.py,
which parses all the received zeromq messages and sends the data to SensorSafe.

Dependencies:

* [Zeromq](http://www.zeromq.org/intro:get-the-software)
* [PySNMP](http://pysnmp.sourceforge.net/quickstart.html)

------------------------------------------------------------------------------

LabSenseSupervisor
------------------

LabSenseSupervisor contains a supervisord.conf file that is meant to be used
with [SuperVisor](http://supervisord.org/). Supervisor allows users LabSense to
monitor and control all the processes that are running (LabSenseZwave,
LabSensePowerMonitor, LabSenseRaritan, LabSenseServer, LabSenseForwarder).

------------------------------------------------------------------------------

Hardware Requirements
====================

This software is running on a [Guruplug Server](http://www.globalscaletechnologies.com/t-guruplugdetails.aspx) with an
[Aeon Labs Z-stick](http://www.aeon-labs.com/site/products/view/2/). 
The sensors that interact with the Z-stick include:

* [Aeon Labs Door/Window Sensor](http://www.aeon-labs.com/site/products/view/1/)
* [Homeseer MultiSensor](http://store.homeseer.com/store/HomeSeer-HSM100-S2-Z-Wave-Multi-Sensor-P1189C57.aspx)
* [Aeon Labs SmartSwitch](http://www.aeon-labs.com/site/products/view/5/)
* [Veris E30A](http://www.powermeterstore.com/crm_uploads/veris_e30_panelboard_monitoring_system_installation_guide.pdf)
* [Raritan PX8](http://www.raritan.com/support/dominion-px/v1.3.5/user-guides/english/DPX-0L-v1.3.5-E.pdf),


------------------------------------------------------------------------------

Installation
===========

General Installation (Needed by all components)
----------------------------------------------

1. Install Zeromq by following directions at http://www.zeromq.org/intro:get-the-software

LabSenseZwave Installation
--------------------------

1. Install needed development headers for open-zwave:

    <pre>
    sudo apt-get install libudev-dev
    </pre>

2. Get the open-zwave source code using svn by running:

    <pre>
    svn checkout http://open-zwave.googlecode.com/svn/trunk/ open-zwave/
    </pre>

3. Navigate to open-zwave/cpp/examples/linux/
4. Get the source code for this project using git or download it:

    <pre>
    git clone git@github.com:jtsao22/LabSense.git
    </pre>

    The LabSense Project should now be at open-zwave/cpp/examples/linux/LabSense.

5. Navigate to LabSense/LabSenseZwave/
6. Pair the Z-stick with the sensors:

    1. Push the button on the Z-stick. The light on the Z-stick should blink. 
    2. Push the button on the sensor. The light on the Z-stick should stay lit for a few seconds and then start blinking again. 
    3. The sensor has been paired and the Z-stick is ready for the next sensor. Start at step 2 for the next sensor. 
    4. When all sensors have been paired, push the button on the Z-stick and the light should stop blinking.

7. Make the code and run the executable

    <pre>
    make 
    ./LabSenseZwave [serial port]
    </pre>

    To figure out what serial port, please plug the Z-stick into the Guruplug and run dmesg. A line similar to the following should specify the port:

    <pre>
    "cp210x converter now attached to [serial port]"
    </pre>

    Unless other usb devices are plugged in, usually the serial port is /dev/ttyUSB0. 

LabSensePowerMonitor Installation
---------------------------------

1. Make the files and run the executable:
    <pre>
    make
    ./TCPModbusClient r all
    </pre>

LabSenseRaritan Installation
----------------------------

1. Install py-snmp:

    <pre>
    easy_install pysnmp
    </pre>

2. Change the Raritan Server address in raritan.py:

    <pre>
    RARITAN_IP_ADDRESS = '[Insert ip address]'
    </pre>

3. Run the python file:

    <pre>
    python raritan.py
    </pre>

LabSenseServer Installation
---------------------------
This is still in beta, please do not try installing this just yet.


LabSenseForwarder Installation
------------------------------

The previous steps are used for local viewing of the data coming of the sensors. If an online graphical view of the
sensor data is required, more code has been implemented to send the data to [SensorSafe](https://128.97.93.29/):

1. Install python bindings by following directions at http://www.zeromq.org/bindings:python
2. Register for a SensorSafe account and take note of the API key.
3. To send the data to SensorSafe, run the python script sendToSensorSafe.py while running the LabSenseZwave
executable:

    <pre>
    python sendToSensorSafe.py [api-key] 
    </pre>

    [api-key] is the API key given during SensorSafe registration.
    More options are available:
        -f [frequency] is optional and specifies how often to send data to SensorSafe.
        -e send event-driven measurement immediately
        -v verbose mode
    The usage details can be found by using "-h" or "--help"

    (Either run this in a separate ssh session/terminal or run one of the processes in the background).

    To see more information about the inner workings of sendToSensorSafe.py, 
    you can use pydoc (installed with python):

    <pre>
    pydoc sendToSensorSafe
    </pre>

4. The script will send to SensorSafe as soon as all variables have been initialized (temperature, luminance, and
motion_timeout), which make take some time depending on the wake-up interval of the Homeseer Multisensor (programmed to
be every 6 minutes).
Upon successful upload to SensorSafe, a message similar to the following will
show up if verbose mode is used:

    <pre>
    200 OK
    [('transfer-encoding', 'chunked'), ('vary', 'Accept-Encoding'), ('server', 'Apache/2.2.11 (Ubuntu) mod_ssl/2.2.11
    OpenSSL/0.9.8g mod_wsgi/2.3 Python/2.6.2'), ('connection', 'close'), ('date', 'Tue, 10 Apr 2012 19:47:03 GMT'),
    ('access-control-allow-origin', '*'), ('content-type', 'text/html; charset=utf-8')]
    Upload successful (Collection name: sandbox, Requested by sandbox
    </pre>

5. You can then see the data on SensorSafe by signing in, pressing access data, selecting data channels, and pressing Show Data. 


LabSenseSupervisor Installation
---------------------------------
LabSenseSupervisor requires that everything else is installed correctly. To use
this, you must install supervisor by using easy_install:

    easy_install supervisor

Then, modify the supervisord.conf file on line 26 with your API-KEY:

    command=python ../LabSenseForwarder/sendToSensorSafe.py [API-KEY] -f 2

Then, run supervisor and all the processes will be run:

    supervisord -c supervisord.conf

To check if the processes are being run, you can look at the website hosted
locally at 0.0.0.0:9001 by using any web browser. You can also look in the logs
folder where you will find logs for each of the different components of LabSense.

------------------------------------------------------------------------------

By Jason Tsao
