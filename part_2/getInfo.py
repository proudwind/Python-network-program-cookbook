import socket

def getMachineInfo():
	hostname = socket.gethostname()
	ipAddress = socket.gethostbyname(hostname)
	print "Host name: %s" % hostname
	print "IP address: %s" % ipAddress

def getRemoteMachineInfo(remoteHost):
	try:
		print 'IP address: %s' % (socket.gethostbyname(remoteHost))
	except socket.error, errMsg:
		print '%s: %s' % (remoteHost, errMsg)

def findServiceName(protocolName, ports):
	for port in ports:
		service = socket.getservbyport(port, protocolName)
		print 'Port: %s => service name: %s' % (port, service)
	

if __name__ == '__main__':
	getMachineInfo()
	#getRemoteMachineInfo('www.python.org')
	#findServiceName('tcp', [80, 8080, 445, 2049, 873, 3306, 22])
