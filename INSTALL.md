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

