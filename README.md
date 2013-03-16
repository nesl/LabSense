LabSense
========

This project involves sensing many different characteristics about a lab (i.e.
ambient temperature, electricity, water, occupancy) and making the data
available in an intuitive interface. There are several components to the
project and can function on their own. Each component is assigned to its own
directory. 

------------------------------------------------------------------------------
Devices
=========

LabSenseServer
--------------

LabSenseServer receives event-driven data from Door Sensors and Motion Sensors.
The Door and Motion Sensors talk using a wireless protocol called Zwave. The
Vera Lite/Vera 2 receive this data and send a post request to the
LabSenseServer, which then forwards the data on to assigned data sinks.

LabSenseModbus/Eaton and LabSenseModbus/Veris
--------------------------------------------

LabSenseModbus contains the code to read data from the Veris E30A Power Panel
Monitor and the Eaton Power Monitor. The code is based on the Modbus RTU
Protocol, which involves accessing memory-mapped registers through register-read
or register-write request messages.

LabSenseRaritan
---------------

LabSenseRaritan contains the code to read data from the Raritan PX8 Power
distribution unit. The data is read using the SNMP (Smiple Network Management
Protocol) protocol.

LabSenseZwave
--------------
LabSenseZwave contains the code to read data from the SmartSwitch and the
LightSensor and TemperatureSensor of the 3-in-1 HSM MultiSensor.

Hardware Requirements
====================

The sensors that interact with LabSense include:

* [Aeon Labs Door/Window Sensor](http://aeotec.com/z-wave-door-window-sensor)
* [Homeseer MultiSensor](http://store.homeseer.com/store/HomeSeer-HSM100-S2-Z-Wave-Multi-Sensor-P1189C57.aspx)
* [Aeon Labs SmartSwitch](http://aeotec.com/z-wave-plug-in-switch)
* [Veris E30A](http://www.powermeterstore.com/crm_uploads/veris_e30_panelboard_monitoring_system_installation_guide.pdf)
* [Eaton IQ260](http://www.eaton.com/Eaton/ProductsServices/Electrical/ProductsandServices/PowerQualityandMonitoring/PowerandEnergyMeters/IQ250260/index.htm)
* [Raritan PX8](http://www.raritan.com/support/dominion-px/v1.3.5/user-guides/english/DPX-0L-v1.3.5-E.pdf),
* [Vera Lite](https://shop.micasaverde.com/index.php/vera-1/veralite.html)

Installation
===========

See the INSTALL.md file for installation instructions.
