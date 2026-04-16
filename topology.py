"""
Packet Drop Simulator - Mininet Topology
Author: VIJAY SURIYA P (PES1UG24AM320)
Course: UE24CS252B - Computer Networks
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel


class PacketDropTopo(Topo):
    """
    Topology:
        h1 (10.0.0.1) ---|
        h2 (10.0.0.2) ---+--- s1 --- POX Controller
        h3 (10.0.0.3) ---|
        h4 (10.0.0.4) ---|

    DROP:  h1 -> h3  (blocked by OpenFlow rule)
    ALLOW: all other pairs
    """

    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)


def run():
    setLogLevel('info')
    topo = PacketDropTopo()
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633),
        switch=OVSSwitch
    )
    net.start()
    print("\n" + "="*55)
    print("  Packet Drop Simulator - Topology Ready")
    print("="*55)
    print("  h1=10.0.0.1  h2=10.0.0.2  h3=10.0.0.3  h4=10.0.0.4")
    print("  DROP RULE: h1 -> h3  |  All others: ALLOWED")
    print("="*55)
    print("\n  Test commands:")
    print("    h1 ping -c 4 h2    # SHOULD SUCCEED")
    print("    h1 ping -c 4 h3    # SHOULD FAIL (dropped)")
    print("    pingall            # full test\n")
    CLI(net)
    net.stop()


topos = {'droptopo': PacketDropTopo}

if __name__ == '__main__':
    run()
