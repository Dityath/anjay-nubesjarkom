from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink, Link
from mininet.node import CPULimitedHost
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import os

class MyTopo(Topo):
	def __init__(self, **opts):
		Topo.__init__(self, **opts)
		
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		
		r1 = self.addHost('r1')
		r2 = self.addHost('r2')
		r3 = self.addHost('r3')
		r4 = self.addHost('r4')
		
		curr_buff_size = 100
		
		bw1000 = {"bw": 1, "max_queue_size" : curr_buff_size, "use_htb" : True}
		bw500 = {"bw": 0.5, "max_queue_size" : curr_buff_size, "use_htb" : True}
		
		self.addLink(h1, r1, intfName1 = 'h1-eth0', intfName2 = 'r1-eth0', cls = TCLink, **bw1000)
		self.addLink(h1, r2, intfName1 = 'h1-eth1', intfName2 = 'r2-eth1', cls = TCLink, **bw1000)
		
		self.addLink(h2, r3, intfName1 = 'h2-eth0', intfName2 = 'r3-eth0', cls = TCLink, **bw1000)
		self.addLink(h2, r4, intfName1 = 'h2-eth1', intfName2 = 'r4-eth1', cls = TCLink, **bw1000)
		
		self.addLink(r1, r3, intfName1 = 'r1-eth1', intfName2 = 'r3-eth1', cls = TCLink, **bw500)
		self.addLink(r1, r4, intfName1 = 'r1-eth2', intfName2 = 'r4-eth2', cls = TCLink, **bw1000)
		
		self.addLink(r2, r3, intfName1 = 'r2-eth2', intfName2 = 'r3-eth2', cls = TCLink, **bw1000)
		self.addLink(r2, r4, intfName1 = 'r2-eth0', intfName2 = 'r4-eth0', cls = TCLink, **bw500)

def runTopo():
	os.system("mn -c")
	
	net = Mininet(topo = MyTopo(), link =TCLink, host = CPULimitedHost)
	net.start()
	
	net['r1'].cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	net['r2'].cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	net['r3'].cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	net['r4'].cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	
	net['h1'].cmd("ifconfig h1-eth0 0")
	net['h1'].cmd("ifconfig h1-eth1 0")
	net['h1'].cmd("ifconfig h1-eth0 192.168.0.1 netmask 255.255.255.0")
	net['h1'].cmd("ifconfig h1-eth1 192.168.5.1 netmask 255.255.255.0")
	
	net['h2'].cmd("ifconfig h2-eth0 0")
	net['h2'].cmd("ifconfig h2-eth1 0")
	net['h2'].cmd("ifconfig h2-eth0 192.168.2.1 netmask 255.255.255.0")
	net['h2'].cmd("ifconfig h2-eth1 192.168.3.1 netmask 255.255.255.0")
	
	net['r1'].cmd("ifconfig r1-eth0 0")
	net['r1'].cmd("ifconfig r1-eth1 0")
	net['r1'].cmd("ifconfig r1-eth2 0")
	net['r1'].cmd("ifconfig r1-eth0 192.168.0.2 netmask 255.255.255.0")
	net['r1'].cmd("ifconfig r1-eth1 192.168.1.1 netmask 255.255.255.0")
	net['r1'].cmd("ifconfig r1-eth2 192.168.7.1 netmask 255.255.255.0")
	
	net['r2'].cmd("ifconfig r2-eth0 0")
	net['r2'].cmd("ifconfig r2-eth1 0")
	net['r2'].cmd("ifconfig r2-eth2 0")
	net['r2'].cmd("ifconfig r2-eth0 192.168.5.1 netmask 255.255.255.0")
	net['r2'].cmd("ifconfig r2-eth1 192.168.4.2 netmask 255.255.255.0")
	net['r2'].cmd("ifconfig r2-eth2 192.168.6.1 netmask 255.255.255.0")
	
	net['r3'].cmd("ifconfig r3-eth0 0")
	net['r3'].cmd("ifconfig r3-eth1 0")
	net['r3'].cmd("ifconfig r3-eth2 0")
	net['r3'].cmd("ifconfig r3-eth0 192.168.1.2 netmask 255.255.255.0")
	net['r3'].cmd("ifconfig r3-eth1 192.168.3.2 netmask 255.255.255.0")
	net['r3'].cmd("ifconfig r3-eth2 192.168.6.2 netmask 255.255.255.0")
	
	net['r4'].cmd("ifconfig r4-eth0 0")
	net['r4'].cmd("ifconfig r4-eth1 0")
	net['r4'].cmd("ifconfig r4-eth2 0")
	net['r4'].cmd("ifconfig r4-eth0 192.168.4.2 netmask 255.255.255.0")
	net['r4'].cmd("ifconfig r4-eth1 192.168.3.2 netmask 255.255.255.0")
	net['r4'].cmd("ifconfig r4-eth2 192.168.7.2 netmask 255.255.255.0")
	
	net['h1'].cmd("ip rule add from 192.168.0.1 table 1")
	net['h1'].cmd("ip rule add from 192.168.5.1 table 2")
	net['h1'].cmd("ip route add 192.168.0.0/24 dev h1-eth0 scope link table 1")
	net['h1'].cmd("ip route add default via 192.168.0.2 dev h1-eth0 table 1")
	net['h1'].cmd("ip route add 192.168.5.0/24 dev h1-eth1 scope link table 2")
	net['h1'].cmd("ip route add default via 192.168.5.1 dev h1-eth1 table 2")
	net['h1'].cmd("ip route add default scope global nexthop via 192.168.0.2 dev h1-eth0")
	
	net['h2'].cmd("ip rule add from 192.168.2.2 table 3")
	net['h2'].cmd("ip rule add from 192.168.3.1 table 4")
	net['h2'].cmd("ip route add 192.168.2.0/24 dev h2-eth0 scope link table 3")
	net['h2'].cmd("ip route add default via 192.168.4.2 dev h2-eth0 table 3")
	net['h2'].cmd("ip route add 192.168.3.0/24 dev h2-eth1 scope link table 4")
	net['h2'].cmd("ip route add default via 192.168.3.2 dev h2-eth1 table 4")
	net['h2'].cmd("ip route add default scope global nexthop via 192.168.2.1 dev h2-eth0")
	
	net['r1'].cmd("route add -net 192.168.6.0/24 gw 192.168.1.2")
	net['r1'].cmd("route add -net 192.168.2.0/24 gw 192.168.1.2")
	net['r1'].cmd("route add -net 192.168.3.0/24 gw 192.168.1.2")
	net['r1'].cmd("route add -net 192.168.4.0/24 gw 192.168.7.2")
	net['r1'].cmd("route add -net 192.168.3.0/24 gw 192.168.7.2")
	net['r2'].cmd("route add -net 192.168.7.0/24 gw 192.168.4.1")
	net['r2'].cmd("route add -net 192.168.3.0/24 gw 192.168.4.1")
	net['r2'].cmd("route add -net 192.168.0.0/24 gw 192.168.4.1")
	net['r2'].cmd("route add -net 192.168.2.0/24 gw 192.168.7.2")
	net['r2'].cmd("route add -net 192.168.2.0/24 gw 192.168.7.2")
	
	net['r3'].cmd("route add -net 192.168.5.0/24 gw 192.168.6.1")
	net['r3'].cmd("route add -net 192.168.4.0/24 gw 192.168.6.1")
	net['r3'].cmd("route add -net 192.168.0.0/24 gw 192.168.1.1")
	net['r3'].cmd("route add -net 192.168.3.0/24 gw 192.168.1.1")
	net['r3'].cmd("route add -net 192.168.7.0/24 gw 192.168.1.1")
	
	net['r4'].cmd("route add -net 192.168.6.0/24 gw 192.168.4.2")
	net['r4'].cmd("route add -net 192.168.5.0/24 gw 192.168.4.2")
	net['r4'].cmd("route add -net 192.168.2.0/24 gw 192.168.4.2")
	net['r4'].cmd("route add -net 192.168.0.0/24 gw 192.168.7.1")
	net['r4'].cmd("route add -net 192.168.1.0/24 gw 192.168.7.1")
	
	print("CLO 2\n")
	
	net.pingAll()
	
	CLI(net)
	
	net.stop()


if "__main__" == __name__:
	setLogLevel("info")
	runTopo()
