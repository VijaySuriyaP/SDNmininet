"""
Packet Drop Simulator - POX SDN Controller
Author: VIJAY SURIYA P (PES1UG24AM320)
Course: UE24CS252B - Computer Networks

Description:
    POX-based OpenFlow controller that:
    - Installs DROP rules for h1 -> h3 traffic
    - Acts as L2 learning switch for all other flows
    - Re-installs rules on every switch connect (regression safe)

Usage:
    Copy this file to ~/pox/ext/packet_drop_controller.py
    Then run: python ~/pox/pox.py packet_drop_controller
"""

from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr

log = core.getLogger()

# ─────────────────────────────────────────
#  DROP RULE CONFIGURATION
# ─────────────────────────────────────────
DROP_SRC_IP = "10.0.0.1"   # h1
DROP_DST_IP = "10.0.0.3"   # h3

DROP_PRIORITY    = 100
FORWARD_PRIORITY = 10


class PacketDropSwitch(object):
    """One instance per connected switch."""

    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}
        connection.addListeners(self)
        self._install_table_miss()
        self._install_drop_rule()

    def _install_drop_rule(self):
        """DROP rule: h1->h3, empty actions = drop in OpenFlow."""
        msg = of.ofp_flow_mod()
        msg.priority = DROP_PRIORITY
        msg.match.dl_type = 0x0800
        msg.match.nw_src  = IPAddr(DROP_SRC_IP)
        msg.match.nw_dst  = IPAddr(DROP_DST_IP)
        # No actions appended = DROP
        self.connection.send(msg)
        log.info("[DROP RULE INSTALLED] %s -> %s  priority=%d",
                 DROP_SRC_IP, DROP_DST_IP, DROP_PRIORITY)

    def _install_table_miss(self):
        """Send unmatched packets to controller."""
        msg = of.ofp_flow_mod()
        msg.priority = 0
        msg.match = of.ofp_match()
        msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
        self.connection.send(msg)

    def _handle_PacketIn(self, event):
        """L2 learning switch for all non-dropped flows."""
        pkt     = event.parsed
        if not pkt.parsed:
            return

        in_port = event.port
        self.mac_to_port[pkt.src] = in_port

        if pkt.dst in self.mac_to_port:
            out_port = self.mac_to_port[pkt.dst]
        else:
            out_port = of.OFPP_ALL

        if out_port != of.OFPP_ALL:
            msg = of.ofp_flow_mod()
            msg.priority     = FORWARD_PRIORITY
            msg.match        = of.ofp_match.from_packet(pkt, in_port)
            msg.idle_timeout = 30
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=out_port))
            msg.data = event.ofp
            self.connection.send(msg)
        else:
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=of.OFPP_ALL))
            self.connection.send(msg)

        ip = pkt.find('ipv4')
        if ip:
            log.debug("[PKT-IN] %s->%s port=%d->%s",
                      ip.srcip, ip.dstip, in_port,
                      str(out_port) if out_port != of.OFPP_ALL else "FLOOD")


class PacketDropController(object):
    def __init__(self):
        core.openflow.addListeners(self)
        log.info("=" * 50)
        log.info("  Packet Drop Simulator - POX Controller")
        log.info("  DROP RULE: %s -> %s", DROP_SRC_IP, DROP_DST_IP)
        log.info("=" * 50)

    def _handle_ConnectionUp(self, event):
        log.info("Switch connected: %s", dpidToStr(event.dpid))
        PacketDropSwitch(event.connection)


def launch():
    core.registerNew(PacketDropController)
