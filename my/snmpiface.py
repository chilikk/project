from pysnmp.entity.rfc3413.oneliner import cmdgen
from pyasn1.type.univ import ObjectIdentifier

class SnmpIface(object):
	""" Object handles the connection with an SNMP-enabled object and 
	provides an interface to this object as simple as getting an object, 
	a set of objects or a subtree in one line  """

	defaults = { 	'host'		: '192.168.1.10', # IP address to connect to
			'port'		: 161,			# udp port to connect to
			'securityName' 	: 'EP2300_student', # SNMPv3 Security Name
			'authKey'	: 'netmanagement', # SNMPv3 Authentication Key
			'privKey'	: 'netmanagement', # SNMPv3 Privacy Key
			'authProtocol'	: 'MD5', # protocol used to verify authenticity
			'privProtocol'	: 'no' } # protocol used to achieve privacy
	
	oid_ipRouteNextHop = "1.3.6.1.2.1.4.21.1.7"
	oid_sysName = "1.3.6.1.2.1.1.5.0"
	oid_ifNumber = "1.3.6.1.2.1.2.1.0"
	oid_ifDescr = "1.3.6.1.2.1.2.2.1.2"
	oid_ipAdEntAddr = "1.3.6.1.2.1.4.20.1.1"
	oid_ifInOctets = "1.3.6.1.2.1.2.2.1.10" #ifInUcastPackets, ifInNUcastPackets, ifInDiscards, ifInErrors follow, can be read by getbulk

	authProtocolsList = { 	'MD5' : cmdgen.usmHMACMD5AuthProtocol, # binding of human-readable name of a protocol to its system identifier
				'SHA' : cmdgen.usmHMACSHAAuthProtocol,
				'no'  : cmdgen.usmNoAuthProtocol }

	privProtocolsList = {	'DES'     : cmdgen.usmDESPrivProtocol, # binding of human-readable name of a protocol to its system identifier
				'3DES'    : cmdgen.usm3DESEDEPrivProtocol,
				'AES'     : cmdgen.usmAesCfb128Protocol,
				'AES192'  : cmdgen.usmAesCfb192Protocol,
				'AES256'  : cmdgen.usmAesCfb256Protocol,
				'no'      : cmdgen.usmNoPrivProtocol }

	def __init__(self,**kwargs):
		# every parameter can be initialized through kwargs, otherwise set to default
		self.host = kwargs['host'] if 'host' in kwargs else self.defaults['host']
		port = int(kwargs['port']) if 'port' in kwargs else int(self.defaults['port'])

		securityName = kwargs['securityName'] if 'securityName' in kwargs else self.defaults['securityName']
		authKey = kwargs['authKey'] if 'authKey' in kwargs else	self.defaults['authKey']
		privKey = kwargs['privKey'] if 'privKey' in kwargs else	self.defaults['privKey']
		authProtocol = self.authProtocolsList[kwargs['authProtocol'] if 'authProtocol' in kwargs else self.defaults['authProtocol'] ]
		privProtocol = self.privProtocolsList[kwargs['privProtocol'] if 'privProtocol' in kwargs else self.defaults['privProtocol'] ]

		authParameters = {	'authProtocol': authProtocol,
					'privProtocol': privProtocol }
		if authProtocol != self.authProtocolsList['no']:
			authParameters['authKey'] = authKey
		if privProtocol != self.privProtocolsList['no']:
			authParameters['privKey'] = privKey
		self.authentication = cmdgen.UsmUserData(securityName, **authParameters)

		transportParameters = (self.host,port)
		self.transport = cmdgen.UdpTransportTarget(transportParameters)
	
	def test(self):
		""" test if class works as expected: prints the system name of an object """
		try:
			print "sysName: %s" % self.getObject(self.oid_sysName)
		except SnmpException, e:
			print e.message
			return
	
	def parseResponse(self, response,oid=False):
		""" transform the response from the binary representation to the human-readable format """
		result={}
		for row in response:
			for name,value in row:
				if not oid or oid == name.prettyPrint()[:len(oid)]:
					result[name.prettyPrint()]=value.prettyPrint()
		return result

	def getSubtree(self,oid):
		""" get the whole subtree with getnext, like snmpwalk """
		errorIndication, errorStatus, errorIndex, response = cmdgen.CommandGenerator().nextCmd(self.authentication, self.transport, ObjectIdentifier(oid).asTuple())
		if not response:
			errorDescription = "%s: %s %s" % (errorIndex, errorStatus, errorIndication)
			raise SnmpException('An error occured: '+errorDescription)
		return self.parseResponse(response)

	def getObject(self,oid):
		""" get the single object with get """
		errorIndication, errorStatus, errorIndex, response = cmdgen.CommandGenerator().getCmd(self.authentication, self.transport, ObjectIdentifier(oid).asTuple())
		if not response:
			errorDescription = "%s: %s %s" % (errorIndex, errorStatus, errorIndication)
			raise SnmpException('An error occured: '+errorDescription)
		result = self.parseResponse((response,),oid)
		if result:
			return result.values()[0]
		raise Exception('Object with given OID does not exist or something went wrong!')

	def getBulk(self, oid, bulkSize, **kwargs):
		""" get the set of object with getbulk. should be passed "dontmatch=1" if the objects are not within same subtree """
		errorIndication, errorStatus, errorIndex, response = cmdgen.CommandGenerator().bulkCmd(self.authentication, self.transport, 0, bulkSize+1, ObjectIdentifier(oid).asTuple())
		if not response:
			errorDescription = "%s: %s %s" % (errorIndex, errorStatus, errorIndication)
			raise SnmpException('An error occured: '+errorDescription)
		if 'dontmatch' in kwargs and kwargs['dontmatch']==1:
			return self.parseResponse(response)
		else:
			return self.parseResponse(response,oid)


class SnmpException(Exception):
	""" Error while trying to query an SNMP object """
	pass
