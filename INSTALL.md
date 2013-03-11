Installation
============

1. Install Distribute and Pip to install python packages. If you have pip
already, you can skip this step:
    <pre>
    curl -O http://python-distribute.org/distribute_setup.py && sudo python distribute_setup.py
    curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py && sudo python get-pip.py
    </pre>

2. Create a virtual environment using virtualenv and get the code:
    <pre>
    virtualenv LabSense
    cd LabSense
    git clone git@github.com:jtsao22/LabSense.git
    source bin/activate
    </pre>

3. Install dependencies virtualenv and py-snmp
    <pre>
    sudo pip install -r requirements.txt
    </pre>

4. In order to use SensorAct, you must create a SensorAct account:

    1. Create a user account by running the following curl command replacing [YOURUSERNAME], [YOURPASSWORD], and [YOUREMAIL]
        <pre>
        curl --request POST \
             --data '{"username": "[YOURUSERNAME]", "password": "[YOURPASSWORD]", "email": "[YOUREMAIL]"}' \
             --header '{"Content-type": "application/json", "Accept": "text/plain"}' \
             --verbose \
             128.97.93.51:9000/user/register
        </pre>

        You should receive a reply similar to the
        following:
        <pre>
            {"apiname":"user/register","statuscode":0,"message":"New Userprofile registered: [YOURUSERNAME]"}
        </pre>

    2. Login and get your Api key:

        <pre>
        curl --request POST \
             --data '{"username": "[YOURUSERNAME]", "password": "[YOURPASSWORD]"}' \
             --header '{"Content-type": "application/json", "Accept": "text/plain"}' \
             --verbose \
             128.97.93.51:9000/user/login
        </pre>

        You should receive a 32 character api key in the reply:
        <pre>
        {"apiname":"user/login","statuscode":0,"message":"[API-KEY]"}
        </pre>
    3. Copy the Api key to the config.json file in the SensorAct section.

5. In order to use Cosm, you must first create an account at www.cosm.com

    1. Navigate to www.cosm.com and follow instructions.
    2. Sign in and click on the "Keys" button on the top right area.
    3. Click the blue "+Key" button.
    4. In the options, enter a Label, Choose "Use any public feed", and make
       Access Prileges set to "all." Then click the orange "Create" button.
    5. Copy the Api key to the config.json file in the Cosm section.

6. If you pla on using Zwave, make sure to set up the Vera 2 hardware correctly
by following this video:


Usage
=====
1. Navigate to the LabSenseHandler directory.

2. Create a config.json file using the config.json.example as a template. This
file is used to specify all the parameters of the different sensors and sinks
you will be using in your LabSense deployment. Please see the last section of
this document for a description of the config.json file. 

3. Start the program by running:
    <pre>
    python main.py config.json
    </pre>

LabSense Configuration
======================

The LabSenseHandler/config.json configuration file tells LabSense all the
parameters it needs to:
    1. Send data to DataSinks:
        * SensorActInterval
        * Cosm
        * Stdout
    2. Retrieve data from Devices:
        * Eaton
        * Veris
        * Raritan
        * SmartSwitch
        * LightSensor
        * TemperatureSensor
        * LabSenseServer, which has two devices:
            * DoorSensor
            * MotionSensor

It is highly recommended that your create your config.json file from the
config.json.example file provided because it provides all the necessary
variables (you simply need to fill in the variables according to your own
configuration).

DataSinks
---------

1. SensorAct Data requirements:
    * IP: IP of SensorAct server 
    * PORT: Port of SensorAct server
    * API_KEY: api key of SensorAct account. See step (4) in installation
                instructions.

2. Cosm Data requirements:
    * API_KEY: api key of Cosm account. See step (5) in the Installation
               instructions.
    * user_name: Cosm user name (needed for checking what feeds are already
                 created).

3. Stdout requirements:
    * None are needed, so leave this empty. The reason why this is left in is
      because if a device wants to send to stdout, the datasink should be
      specified in the file.

4. Device requirements (Eaton, Veris, Raritan, SmartSwitch, LightSensor,
TemperatureSensor, DoorSensor, and MotionSensor):
    * name: This is the name you give your device. It must be **unique** and will be
            used for the Cosm channel name and SensorAct devicename. 
    * IP: IP of the device. Note:
        * Eaton, Veris, SmartSwitch, TemperatureSensor all have IP's from which to query. 
        * LabSenseServer devices (DoorSensor and MotionSensor) should both specify the IP of the computer you are running LabSense on. This IP is used for SensorAct, which requires an IP for the devices sending data.
    * PORT: Port of the device
    * location: This is used by SensorAct. Simply give a string specifying your location.
    * latitude, longitude: This is used by SensorAct. Give location details about your location.
    * channels: This is a list of channels you would like to retrieve from  the * device. All devices currently have all channels specified by default in * the config.json.example file.
    * sinterval: This is the amount of time between each sampling of the device. 
    * SensorAct, Cosm, Stdout: This are boolean values: true means send to the datasink, false means do not.
    * SensorActInterval, CosmInterval, StdoutInterval: The amount of time between each sending of the data.

5. LabSenseServer requirements.
    * name: This is the name of your LabSenseServer. It must be **unique** and is identified by this name (you can have several LabSenseServer's).
    * PORT: This is the port on your computer/server that you would like to
    serve the server on. Event-driven Zwave Devices (currently Door Sensor and
    Motion Sensor) send data to this server, which then forwards the data to the
    different datasinks according to the rates specified. 
    * API_KEY: This is an agreed upon API_KEY that is specified in the config file and in the json sent from the Zwave Device.
    * Sensors: This can contain any number of MotionSensors and DoorSensors with configurations exactly the same as other device requirements except a PORT is not required.

6. Setting Up Zwave
    * Zwave Devices include: LightSensor, TemperatureSensor, SmartSwitch, DoorSensor, and MotionSensor.
    * There are two groups of Zwave Devices:
        1. Polling based: LightSensor, TemperatureSensor, and SmartSwitch.
            * The "name" field must be the same name given to the sensor on the
            Vera 2 webpage. To check/change the name on the Vera 2 webpage, go
            to the IP of your Vera and click on the "Devices" tab. Check what
            the name of the LightSensor is and make sure it matches with the
            "name" field of the sensor in question. See the following image:

            ![Zwave name]([1])

        2. Event-driven: DoorSensor and MotionSensor.
            For these sensors, lua code must be written by the Vera sensors to
            send to the LabSenseServer you will host on your computer.

            Setup instructions:
            1. Navigate to the Vera 2 webpage.
            2. Click on the "Apps" tab and then the "Develop Apps" subtab.
            3. Click on "Edit Startup Lua" and copy/paste the "startup.lua" code
            in Devices/LabSenseServer/lua/startup.lua to the box and click "Go."
            4. Click the red "Save" button on the top right.
            ![Edit startup]([2])
            5. Click on the "Automation" tab, and click on the settings page of
            your scene. 
            6. Click on the "Triggers" tab and add three triggers: 
                1. Door opened with the Door Sensor 
                    Configure like the following:
                    ![Config]([3])
                    Add code by clicking on "Luup Event" and copy/pasting code
                    from Devices/LabSenseServer/lua/door_opened_luup_event.lua.
                2. Door closed with the Door Sensor
                    Configure like the following:
                    ![Config]([4])
                    Add code by clicking on "Luup Event" and copy/pasting code
                    from Devices/LabSenseServer/lua/door_closed_luup_event.lua.
                3. Motion Detected with the Motion Sensor
                    Configure like the following:
                    ![Config]([5])
                    Add code by clicking on "Luup Event" and copy/pasting code
                    from Devices/LabSenseServer/lua/motion_detected_luup_event.lua.
                4. **IMPORTANT** For all Luup events, make sure to change the local api_key
                line to reflect the same API_KEY specified in the API_KEY field
                of LabSenseServer in the config.json file!

                    
            
    
[1]: https://raw.github.com/jtsao22/LabSense/master/imgs/LabSenseZwaveInstall.jpg
[2]: https://raw.github.com/jtsao22/LabSense/master/imgs/LabSenseZwaveInstallStartupLua.jpg
[3]: https://raw.github.com/jtsao22/LabSense/master/imgs/DoorOpenedTrigger.jpg
[4]: https://raw.github.com/jtsao22/LabSense/master/imgs/DoorClosedTrigger.jpg
[5]: https://raw.github.com/jtsao22/LabSense/master/imgs/MotionDetectedTrigger.jpg
