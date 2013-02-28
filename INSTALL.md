Installation
============

1. Install Pip:
    <pre>
    curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py && sudo python get-pip.py
    </pre>

2. Source the virtual environment
    <pre>
    source bin/activate
    </pre>

3. Install dependencies virtualenv and py-snmp
    <pre>
    pip install -r requirements.txt
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
