import socket
from binascii import hexlify

def convert_ip4_address(*ips):
	for ip in ips:
		packedIpAddr = socket.inet_aton(ip)
		unpackedIpAddr = socket.inet_ntoa(packedIpAddr)
		print 'IP Address: %s => Packed: %s, Unpacked: %s' % (ip, hexlify(packedIpAddr), unpackedIpAddr)

if __name__ == '__main__':
	convert_ip4_address('192.168.0.1', '127.0.0.1')
