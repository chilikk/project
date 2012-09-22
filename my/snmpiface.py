from pysnmp.entity.rfc3413.oneliner import cmdgen
from pyasn1.type.univ import ObjectIdentifier

class SnmpIface(object):

	defaults = { 	'host'		: '192.168.1.10',
			'port'		: 161,			
			'securityName' 	: 'EP2300_student',
			'authKey'	: 'netmanagement',
			'privKey'	: 'netmanagement',
			'authProtocol'	: 'MD5',
			'privProtocol'	: 'no' }
	
	oid_ipRouteNextHop = "1.3.6.1.2.1.4.21.1.7"
	oid_sysName = "1.3.6.1.2.1.1.5.0"
	oid_ifNumber = "1.3.6.1.2.1.2.1.0"
	oid_ifDescr = "1.3.6.1.2.1.2.2.1.2"
	oid_ipAdEntAddr = "1.3.6.1.2.1.4.20.1.1"

	authProtocolsList = { 	'MD5' : cmdgen.usmHMACMD5AuthProtocol,
				'SHA' : cmdgen.usmHMACSHAAuthProtocol,
				'no'  : cmdgen.usmNoAuthProtocol }

	privProtocolsList = {	'DES'     : cmdgen.usmDESPrivProtocol,
				'3DES'    : cmdgen.usm3DESEDEPrivProtocol,
				'AES'     : cmdgen.usmAesCfb128Protocol,
				'AES192'  : cmdgen.usmAesCfb192Protocol,
				'AES256'  : cmdgen.usmAesCfb256Protocol,
				'no'      : cmdgen.usmNoPrivProtocol }

	def __init__(self,**kwargs):
		host = kwargs['host'] if 'host' in kwargs else self.defaults['host']
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
		authentication = cmdgen.UsmUserData(securityName, **authParameters)

		transportParameters = (host,port)
		transport = cmdgen.UdpTransportTarget(transportParameters)

		setattr(self.__class__, 'authentication', authentication)
		setattr(self.__class__, 'transport', transport)
		setattr(self.__class__, 'host', host)
	
	def test(self):
		try:
			print "sysName: %s" % self.getObject(self.oid_sysName)
		except SnmpException, e:
			print e.message
			return
	
	def _getObj(self,oid,gettype,**kwargs):
		oid = ObjectIdentifier(oid).asTuple()

		if gettype=='getnext':
			errorIndication, errorStatus, errorIndex, response = cmdgen.CommandGenerator().nextCmd(self.authentication, self.transport, oid)
		elif gettype=='get':
			errorIndication, errorStatus, errorIndex, response = cmdgen.CommandGenerator().getCmd(self.authentication, self.transport, oid)
		elif gettype=='getbulk':
			bulkSize = kwargs['bulkSize'] if 'bulkSize' in kwargs else 1
			errorIndication, errorStatus, errorIndex, response = cmdgen.CommandGenerator().bulkCmd(self.authentication, self.transport, 0, bulkSize, oid)
		else:
			raise Exception('Unknown snmp get type! Should be get|getnext|getbulk')

		if not response:
			errorDescription = "%s: %s %s" % (errorIndex, errorStatus, errorIndication)
			raise SnmpException('An error occured: '+errorDescription)
		
		return response

	def parseResponse(self, response,oid=False):
		print response
		result={}
		for row in response:
			for name,value in row:
				if not oid or oid == name.prettyPrint()[:len(oid)]:
					result[name.prettyPrint()]=value.prettyPrint()
		return result

	def getSubtree(self,oid):
		try:
			response = self._getObj(oid,'getnext')
		except Exception:
			raise
		return self.parseResponse(response)

	def getObject(self,oid):
		try:
			response = self._getObj(oid,'get')
		except Exception:
			raise
		result = self.parseResponse(response,oid)
		if result:
			return result.values()[0]
		raise Exception('Object with given OID does not exist or something went wrong!')

	def getBulk(self, oid, bulkSize):
		try:
			response = self._getObj(oid,'getbulk', bulkSize = bulkSize+1)
		except Exception:
			raise
		return self.parseResponse(response,oid)


class SnmpException(Exception):
	pass
