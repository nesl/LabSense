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

------------------------------------------------------------------------------

Project dependencies:

  * [Django 1.3.1](https://www.djangoproject.com/download/
