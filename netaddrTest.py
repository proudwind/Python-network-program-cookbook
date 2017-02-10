import netaddr

subnet = '10.10.10.0/24'

for ip in netaddr.IPNetwork(subnet):
	print ip
