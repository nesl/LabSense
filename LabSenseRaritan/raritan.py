# GET Command Generator
# Format: Real Power(8, Watts), Voltage(8, millivolts), Current(8, milliamps), PF(8), Reactive Power(8, Watt)
#Written by Younghun Kim(NESL,UCLA)

from pysnmp.entity.rfc3413.oneliner import cmdgen

def Get(ip):
  Value=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  count=0
  errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    # SNMP v1
    #cmdgen.CommunityData('test-agent', 'public', 0),
    # SNMP v2
    cmdgen.CommunityData('admin', 'home3747r'), 
     #cmdgen.CommunityData('admin', 'abcd'), # read-only
    #cmdgen.CommunityData('admin', 'efgh'), # write
    # SNMP v3
#    cmdgen.UsmUserData('test-user', 'authkey1', 'privkey1'),
    cmdgen.UdpTransportTarget((ip, 161)),
    (1,3,6,1,4,1,13742,4,1,2,2,1,4,1),
    (1,3,6,1,4,1,13742,4,1,2,2,1,4,2),
    (1,3,6,1,4,1,13742,4,1,2,2,1,4,3),
    (1,3,6,1,4,1,13742,4,1,2,2,1,4,4),
    (1,3,6,1,4,1,13742,4,1,2,2,1,4,5),
    (1,3,6,1,4,1,13742,4,1,2,2,1,4,6),
    (1,3,6,1,4,1,13742,4,1,2,2,1,4,7),
    (1,3,6,1,4,1,13742,4,1,2,2,1,4,8),
    (1,3,6,1,4,1,13742,4,1,2,2,1,6,1),
    (1,3,6,1,4,1,13742,4,1,2,2,1,6,2),
    (1,3,6,1,4,1,13742,4,1,2,2,1,6,3),
    (1,3,6,1,4,1,13742,4,1,2,2,1,6,4),
    (1,3,6,1,4,1,13742,4,1,2,2,1,6,5),
    (1,3,6,1,4,1,13742,4,1,2,2,1,6,6),
    (1,3,6,1,4,1,13742,4,1,2,2,1,6,7),
    (1,3,6,1,4,1,13742,4,1,2,2,1,6,8),
    (1,3,6,1,4,1,13742,4,1,2,2,1,7,1),
    (1,3,6,1,4,1,13742,4,1,2,2,1,7,2),
    (1,3,6,1,4,1,13742,4,1,2,2,1,7,3),
    (1,3,6,1,4,1,13742,4,1,2,2,1,7,4),
    (1,3,6,1,4,1,13742,4,1,2,2,1,7,5),
    (1,3,6,1,4,1,13742,4,1,2,2,1,7,6),
    (1,3,6,1,4,1,13742,4,1,2,2,1,7,7),
    (1,3,6,1,4,1,13742,4,1,2,2,1,7,8),
    (1,3,6,1,4,1,13742,4,1,2,2,1,9,1),
    (1,3,6,1,4,1,13742,4,1,2,2,1,9,2),
    (1,3,6,1,4,1,13742,4,1,2,2,1,9,3),
    (1,3,6,1,4,1,13742,4,1,2,2,1,9,4),
    (1,3,6,1,4,1,13742,4,1,2,2,1,9,5),
    (1,3,6,1,4,1,13742,4,1,2,2,1,9,6),
    (1,3,6,1,4,1,13742,4,1,2,2,1,9,7),
    (1,3,6,1,4,1,13742,4,1,2,2,1,9,8),
    (1,3,6,1,4,1,13742,4,1,2,2,1,8,1),
    (1,3,6,1,4,1,13742,4,1,2,2,1,8,2),
    (1,3,6,1,4,1,13742,4,1,2,2,1,8,3),
    (1,3,6,1,4,1,13742,4,1,2,2,1,8,4),
    (1,3,6,1,4,1,13742,4,1,2,2,1,8,5),
    (1,3,6,1,4,1,13742,4,1,2,2,1,8,6),
    (1,3,6,1,4,1,13742,4,1,2,2,1,8,7),
    (1,3,6,1,4,1,13742,4,1,2,2,1,8,8)
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
              #print '%s = %s' % (name.prettyPrint(), val.prettyPrint())
              #print '%s' % val.prettyPrint()
              #Value[count]=val.prettyPrint()
              Value[count]=int(val.prettyPrint())
              count = count+1
          return Value

