from pysnmp.entity.rfc3413.oneliner import cmdgen
from pyasn1.type.univ import ObjectIdentifier
from snmpiface import SnmpIface

class SnmpAsyncIface(SnmpIface):
	def _getObj(self,oid,gettype,cb):
		oid = ObjectIdentifier(oid).asTuple()

		if gettype=='getnext':
			cmdgen.AsyncCommandGenerator().asyncNextCmd(self.authentication, self.transport, (oid,), (returnNext,(self.host,oid)))
	
	def getSubtree(self,oid,cb):
		try:
			self._getObj(oid,'getnext',cb)
		except Exception:
			raise
	
	def getObject(self,oid,cb):
		try:
			self._getObj(oid,'get',cb)
		except Exception:
			raise
	
	def getBulk(self,oid,cb):
		try:
			self._getObj(oid,'getbulk',cb)
		except Exception:
			raise
