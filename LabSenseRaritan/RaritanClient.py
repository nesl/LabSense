import time                                 # For timestamping data retrieval

from pysnmp.entity.rfc3413.oneliner import cmdgen       # For getting data over snmp 
class RaritanClient(object):

    def __init__(self, name, IP, PORT, channels):
       self.name = name
       self.devicename = "Raritan"
       self.ip = IP
       self.port = PORT
       self.channels = channels

    # getData Command Generator;
    # Format: Current (8, milliamps), Voltage (8, millivolts), Active Power (Watts),
    # Apparent Power (8, Volt-amps), Power Factor (Percentage)
    def getData(self):
        count=0
        current_time = time.time()
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
        cmdgen.CommunityData('admin', 'abcd'), # read-only
        # SNMP v3
        cmdgen.UdpTransportTarget((self.ip, self.port)),

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
                channel_data = self.mapValues(varBinds)

                device_data = {}
                if channel_data:
                    device_data = {"devicename": self.name,
                                   "device": self.devicename,
                                   "timestamp": current_time,
                                   "channels": channel_data
                                  }
                return device_data

    def mapValues(self, varBinds):
        channel_data = {}
        channel_val_pairs = []
        for name, val in varBinds:
            value = int(val.prettyPrint())
            channel = self.getChannelNameFromNumberChannel(name)
            channel_number = self.getChannelNumber(name)
            channel_val_pair = (channel + str(channel_number), value )
            channel_val_pairs.append(channel_val_pair)
            if channel_number == 8:
                channel_data[channel] = {}
                channel_data[channel]["measurements"] = channel_val_pairs
                channel_data[channel]["units"] = self.getUnitsForChannel(channel)
                channel_val_pairs = []

        return channel_data

    """ Helper functions """

    def getChannelNumber(self, name):
        """ Gets the channel number from the
        second to last channel number. Example Snmp
        name format is:
        1.3.6.1.4.1.13742.4.1.2.2.1.s.n.
        This function find n """
        return int(name[-1])

    def getChannelNameFromNumberChannel(self, name):
        """ Gets the channel name from the
        second to last channel number. Example Snmp
        name format is:
        1.3.6.1.4.1.13742.4.1.2.2.1.s.n.
        This function find s and returns
        the channel name equivalent. """
        number_channel = name[-2]
        channel = ""
        if number_channel == 4:
            channel = "Current"
        elif number_channel == 6:
            channel = "Voltage"
        elif number_channel == 7:
            channel = "ActivePower"
        elif number_channel == 8:
            channel = "ApparentPower"
        elif number_channel == 9:
            channel = "PowerFactor"
        return channel

    def getUnitsForChannel(self, channel):
        units = ""
        if channel == "Voltage":
            units = "mV"
        elif channel == "Current":
            units = "mA"
        elif channel == "ActivePower":
            units = "Watts"
        elif channel == "ApparentPower":
            units = "Volt-Amps"
        elif channel == "PowerFactor":
            units = "None"
        else:
            raise KeyError("No such channel name")

        return units
