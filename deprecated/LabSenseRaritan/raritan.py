import time
import argparse                                             # To parse command line arguments
from SensorAct.SensorActUploader import SensorActUploader   # Upload data to SensorAct
import json                                                 # To read SensorAct configuration

from pysnmp.entity.rfc3413.oneliner import cmdgen

class RaritanReader(object):

    def __init__(self, Raritan_IP, sample_interval):
        self.raritan_ip = Raritan_IP
        self.sample_interval = sample_interval
        self.readLabSenseConfig()

    def readLabSenseConfig(self):
        json_config = open("../LabSenseConfig/config.json")
        config = json.load(json_config)
        #sensorActConfig = config["SensorAct"]
        self.SensorActIP = config["IP"]
        self.SensorActPORT = int(config["PORT"])
        self.SensorActKey = config["API_KEY"]

    # getData Command Generator;
    # Format: Current (8, milliamps), Voltage (8, millivolts), Active Power (Watts),
    # Apparent Power (8, Volt-amps), Power Factor (Percentage)
    def getData(self):
        Value=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        count=0
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
        # SNMP v1
        #cmdgen.CommunityData('test-agent', 'public', 0),
        # SNMP v2
        #cmdgen.CommunityData('admin', 'home3747r'), 
        cmdgen.CommunityData('admin', 'abcd'), # read-only
        #cmdgen.CommunityData('admin', 'efgh'), # write
        # SNMP v3
        cmdgen.UdpTransportTarget((self.raritan_ip, 161)),

        # Current for 8 outlets (milliamps)
        (1,3,6,1,4,1,13742,4,1,2,2,1,4,1),
        (1,3,6,1,4,1,13742,4,1,2,2,1,4,2),
        (1,3,6,1,4,1,13742,4,1,2,2,1,4,3),
        (1,3,6,1,4,1,13742,4,1,2,2,1,4,4),
        (1,3,6,1,4,1,13742,4,1,2,2,1,4,5),
        (1,3,6,1,4,1,13742,4,1,2,2,1,4,6),
        (1,3,6,1,4,1,13742,4,1,2,2,1,4,7),
        (1,3,6,1,4,1,13742,4,1,2,2,1,4,8),

        # Voltage for 8 outlets (millivolts)
        (1,3,6,1,4,1,13742,4,1,2,2,1,6,1),
        (1,3,6,1,4,1,13742,4,1,2,2,1,6,2),
        (1,3,6,1,4,1,13742,4,1,2,2,1,6,3),
        (1,3,6,1,4,1,13742,4,1,2,2,1,6,4),
        (1,3,6,1,4,1,13742,4,1,2,2,1,6,5),
        (1,3,6,1,4,1,13742,4,1,2,2,1,6,6),
        (1,3,6,1,4,1,13742,4,1,2,2,1,6,7),
        (1,3,6,1,4,1,13742,4,1,2,2,1,6,8),

        # Active Power for 8 outlets (Watts)
        (1,3,6,1,4,1,13742,4,1,2,2,1,7,1),
        (1,3,6,1,4,1,13742,4,1,2,2,1,7,2),
        (1,3,6,1,4,1,13742,4,1,2,2,1,7,3),
        (1,3,6,1,4,1,13742,4,1,2,2,1,7,4),
        (1,3,6,1,4,1,13742,4,1,2,2,1,7,5),
        (1,3,6,1,4,1,13742,4,1,2,2,1,7,6),
        (1,3,6,1,4,1,13742,4,1,2,2,1,7,7),
        (1,3,6,1,4,1,13742,4,1,2,2,1,7,8),

        # Apparent Power for 8 outlets (Volt-amps)
        (1,3,6,1,4,1,13742,4,1,2,2,1,8,1),
        (1,3,6,1,4,1,13742,4,1,2,2,1,8,2),
        (1,3,6,1,4,1,13742,4,1,2,2,1,8,3),
        (1,3,6,1,4,1,13742,4,1,2,2,1,8,4),
        (1,3,6,1,4,1,13742,4,1,2,2,1,8,5),
        (1,3,6,1,4,1,13742,4,1,2,2,1,8,6),
        (1,3,6,1,4,1,13742,4,1,2,2,1,8,7),
        (1,3,6,1,4,1,13742,4,1,2,2,1,8,8),

        # Power Factor for 8 outlets (Percentage)
        (1,3,6,1,4,1,13742,4,1,2,2,1,9,1),
        (1,3,6,1,4,1,13742,4,1,2,2,1,9,2),
        (1,3,6,1,4,1,13742,4,1,2,2,1,9,3),
        (1,3,6,1,4,1,13742,4,1,2,2,1,9,4),
        (1,3,6,1,4,1,13742,4,1,2,2,1,9,5),
        (1,3,6,1,4,1,13742,4,1,2,2,1,9,6),
        (1,3,6,1,4,1,13742,4,1,2,2,1,9,7),
        (1,3,6,1,4,1,13742,4,1,2,2,1,9,8)
        )

        if errorIndication:
            return errorIndication
        else:
            if errorStatus:
                return '%s at %s\n' % (
                        errorStatus.prettyPrint(), varBinds[int(errorIndex)-1]
                        )
            else:
                for name, val in varBinds:
                    Value[count]=int(val.prettyPrint())
                    count = count+1
                return Value


    def run(self):
        while True:
            # Retrieve data from Raritan
            data = self.getData()
            timestamp = time.time()
            
            print data
            # There should be 40 results, 5 sets of 8 outlet readings (see
            # raritan.py)
            if len(data) != 40:
                print 'Error from raritan: %s'%data
                continue

            sensorActUploader = SensorActUploader("remote", self.SensorActIP,
                    self.SensorActPORT, self.SensorActKey)
            sensorActUploader.send(data, timestamp)

            # sleep ...
            time.sleep(SAMPLE_INTERVAL)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("IP", help="IP address of Raritan")
    parser.add_argument("SAMPLE_INTERVAL", help="Sampling interval for Raritan")
    args = parser.parse_args()

    SAMPLE_INTERVAL = float(args.SAMPLE_INTERVAL)
    RARITAN_IP_ADDRESS = args.IP
    raritan = RaritanReader(RARITAN_IP_ADDRESS, SAMPLE_INTERVAL)
    raritan.run()
