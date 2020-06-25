# Copyright 2016 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from __future__ import division
import struct
import binascii

import netaddr
from bgp.common import afn
from bgp.common import safn
from bgp.common import constants as bgp_cons
from bgp.message.attribute.nlri import NLRI
from bgp.message.attribute.nlri.mpls_vpn import MPLSVPN


class EVPN(NLRI):
    """
      The format of the EVPN NLRI is as follows:
    +-----------------------------------+
    |    Route Type (1 octet)           |
    +-----------------------------------+
    |     Length (1 octet)              |
    +-----------------------------------+
    | Route Type specific (variable)    |
    +-----------------------------------+
    """

    @classmethod
    def parse(cls, nlri_data):
        nlri_list = []
        while nlri_data:
            route_type = ord(nlri_data[0:1])
            offset = ord(nlri_data[1:2])
            route_value = nlri_data[2: offset + 2]
            route = {}
            if route_type == bgp_cons.BGPNLRI_EVPN_ETHERNET_AUTO_DISCOVERY:
                route = EthernetAutoDiscovery.parse(route_value)
            elif route_type == bgp_cons.BGPNLRI_EVPN_MAC_IP_ADVERTISEMENT:
                route = MacIPAdvertisment.parse(route_value)
            elif route_type == bgp_cons.BGPNLRI_EVPN_INCLUSIVE_MULTICAST_ETHERNET_TAG:
                route = InclusiveMulticastEthernetTag.parse(route_value)
            elif route_type == bgp_cons.BGPNLRI_EVPN_ETHERNET_SEGMENT:
                route = EthernetSegment.parse(route_value)
            elif route_type == bgp_cons.BGPNLRI_EVPN_IP_ROUTE_PREFIX:
                route = IPRoutePrefix.parse(route_value)
            if route:
                nlri_list.append({
                    'type': route_type,
                    'value': route
                })
            nlri_data = nlri_data[offset + 2:]
        return nlri_list

    @classmethod
    def construct(cls, nlri_list):
        nlri_list_hex = b''
        for nlri in nlri_list:
            nlri_hex = b''
            if nlri['type'] == bgp_cons.BGPNLRI_EVPN_ETHERNET_AUTO_DISCOVERY:
                nlri_hex = EthernetAutoDiscovery.construct(value=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_MAC_IP_ADVERTISEMENT:
                nlri_hex = MacIPAdvertisment.construct(value=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_INCLUSIVE_MULTICAST_ETHERNET_TAG:
                nlri_hex = InclusiveMulticastEthernetTag.construct(value=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_ETHERNET_SEGMENT:
                nlri_hex = EthernetSegment.construct(value=nlri['value'])
            elif nlri['type'] == bgp_cons.BGPNLRI_EVPN_IP_ROUTE_PREFIX:
                nlri_hex = IPRoutePrefix.construct(value=nlri['value'])
            if nlri_hex:
                nlri_list_hex += struct.pack('!2B', nlri['type'], len(nlri_hex)) + nlri_hex
        return nlri_list_hex

    @staticmethod
    def signal_evpn_overlay(attr_dict):
        """
        draft-ietf-bess-evpn-overlay-10 changes label encoding if EVPN and encapsulation EC set

        :param attr_dict: bgp attribute dictionary
        """
        evpn_overlay = {'evpn': False, 'encap_ec': False}
        try:
            afi_safi = tuple(attr_dict.get(bgp_cons.BGPTYPE_MP_REACH_NLRI).get('afi_safi'))
            community_ext = attr_dict.get(bgp_cons.BGPTYPE_EXTENDED_COMMUNITY)
        except:
            return evpn_overlay
        if afi_safi == (afn.AFNUM_L2VPN, safn.SAFNUM_EVPN):
            evpn_overlay['evpn'] = True
        if community_ext:
            for ec in community_ext:
                if bgp_cons.BGP_EXT_COM_DICT['encapsulation'] == ec[0]:
                    evpn_overlay['encap_ec'] = True
                    evpn_overlay['encap_value'] = int(ec[1])
        return evpn_overlay


class EthernetAutoDiscovery(MPLSVPN):
    """
    +---------------------------------------+
    |  Route Distinguisher (RD) (8 octets)  |
    +---------------------------------------+
    |Ethernet Segment Identifier (10 octets)|
    +---------------------------------------+
    |  Ethernet Tag ID (4 octets)           |
    +---------------------------------------+
    |  MPLS Label (3 octets)                |
    +---------------------------------------+

    """
    @classmethod
    def parse(cls, value, iswithdraw=False):
        route = dict()
        route['rd'] = cls.parse_rd(value[0:8])
        offset = 8
        route['esi'] = int(binascii.b2a_hex(value[offset: offset+10]), 16)
        offset += 10
        # ethernet tag id
        route['eth_tag_id'] = struct.unpack('!I', value[offset: offset+4])[0]
        offset += 4
        route['label'] = MPLSVPN.parse_mpls_label_stack(value[offset:])
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        # rd
        value_hex = b''
        value_hex += MPLSVPN.construct_rd(value['rd'])
        # esi
        value_hex += b'\x00\x00' + struct.pack('!d', value['esi'])
        # ethernet tag
        value_hex += struct.pack('!I', value['eth_tag_id'])
        value_hex += MPLSVPN.construct_mpls_label_stack(value['label'])
        return value_hex


class MacIPAdvertisment(MPLSVPN):
    """
    +---------------------------------------+
    |  RD (8 octets)                        |
    +---------------------------------------+
    |Ethernet Segment Identifier (10 octets)|
    +---------------------------------------+
    |  Ethernet Tag ID (4 octets)           |
    +---------------------------------------+
    |  MAC Address Length (1 octet)         |
    +---------------------------------------+
    |  MAC Address (6 octets)               |
    +---------------------------------------+
    |  IP Address Length (1 octet)          |
    +---------------------------------------+
    |  IP Address (0, 4, or 16 octets)      |
    +---------------------------------------+
    |  MPLS Label1 (3 octets)               |
    +---------------------------------------+
    |  MPLS Label2 (0 or 3 octets)          |
    +---------------------------------------+
    """

    @classmethod
    def parse(cls, value, iswithdraw=False):
        route = dict()
        # rd
        offset = 8
        route['rd'] = cls.parse_rd(value[0:offset])
        # esi
        route['esi'] = int(binascii.b2a_hex(value[offset: offset+10]), 16)
        offset += 10
        # ethernet tag id
        route['eth_tag_id'] = struct.unpack('!I', value[offset: offset+4])[0]
        offset += 5
        # mac address
        route['mac'] = str(netaddr.EUI(int(binascii.b2a_hex(value[offset: offset+6]), 16)))
        offset += 6
        ip_addr_len = ord(value[offset: offset + 1])
        offset += 1
        # ip address
        if ip_addr_len != 0:
            route['ip'] = str(netaddr.IPAddress(
                int(binascii.b2a_hex(value[offset: offset + int(ip_addr_len / 8)]), 16)))
            offset += int(ip_addr_len / 8)
        # label
        route['label'] = MPLSVPN.parse_mpls_label_stack(value[offset:])
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        # rd
        value_hex = b''
        value_hex += MPLSVPN.construct_rd(value['rd'])
        # esi
        value_hex += b'\x00\x00' + struct.pack('!d', value['esi'])
        # ethernet tag
        value_hex += struct.pack('!I', value['eth_tag_id'])
        # mac address len and address
        mac_hex = b''.join([struct.pack('!B', (int(i, 16))) for i in value['mac'].split("-")])
        value_hex += struct.pack('!B', len(mac_hex) * 8) + mac_hex
        # ip address len and address
        if value.get('ip'):
            ip_hex = netaddr.IPAddress(value['ip']).packed
            value_hex += struct.pack('!B', len(ip_hex) * 8) + ip_hex
        else:
            value_hex += b'\x00'
        if value.get('label'):
            value_hex += MPLSVPN.construct_mpls_label_stack(value['label'])
        return value_hex


class InclusiveMulticastEthernetTag(MPLSVPN):
    """
   +---------------------------------------+
   |  RD (8 octets)                        |
   +---------------------------------------+
   |  Ethernet Tag ID (4 octets)           |
   +---------------------------------------+
   |  IP Address Length (1 octet)          |
   +---------------------------------------+
   |  Originating Router's IP Address      |
   |          (4 or 16 octets)             |
   +---------------------------------------+
    """

    @classmethod
    def parse(cls, value, iswithdraw=False):
        route = dict()
        offset = 8
        route['rd'] = MPLSVPN.parse_rd(value[0:offset])
        route['eth_tag_id'] = struct.unpack('!I', value[offset: offset+4])[0]
        offset += 4
        ip_addr_len = ord(value[offset: offset + 1])
        offset += 1
        # ip address
        if ip_addr_len != 0:
            route['ip'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value[offset: int(offset+ip_addr_len / 8)]), 16)))
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        # rd
        value_hex = b''
        value_hex += MPLSVPN.construct_rd(value['rd'])
        value_hex += struct.pack('!I', value['eth_tag_id'])
        # ip address len and address
        if value.get('ip'):
            ip_hex = netaddr.IPAddress(value['ip']).packed
            value_hex += struct.pack('!B', len(ip_hex) * 8) + ip_hex
        else:
            value_hex += b'\x00'
        return value_hex


class EthernetSegment(MPLSVPN):
    """
   +---------------------------------------+
   |  RD (8 octets)                        |
   +---------------------------------------+
   |Ethernet Segment Identifier (10 octets)|
   +---------------------------------------+
   |  IP Address Length (1 octet)          |
   +---------------------------------------+
   |  Originating Router's IP Address      |
   |          (4 or 16 octets)             |
   +---------------------------------------+

    """
    @classmethod
    def parse(cls, value, iswithdraw=False):
        route = dict()
        offset = 8
        route['rd'] = MPLSVPN.parse_rd(value[0:offset])
        # esi
        route['esi'] = int(binascii.b2a_hex(value[offset: offset+10]), 16)
        offset += 10
        ip_addr_len = ord(value[offset: offset + 1])
        offset += 1
        # ip address
        if ip_addr_len != 0:
            route['ip'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value[offset: offset+ip_addr_len // 8]), 16)))
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        # rd
        value_hex = b''
        value_hex += MPLSVPN.construct_rd(value['rd'])
        # esi
        value_hex += b'\x00\x00' + struct.pack('!d', value['esi'])
        # ip address len and address
        if value.get('ip'):
            ip_hex = netaddr.IPAddress(value['ip']).packed
            value_hex += struct.pack('!B', len(ip_hex) * 8) + ip_hex
        else:
            value_hex += b'\x00'
        return value_hex


class IPRoutePrefix(MPLSVPN):
    """
    # http://tools.ietf.org/html/draft-ietf-bess-evpn-prefix-advertisement-01
    +---------------------------------------+
    |      RD   (8 octets)                  |
    +---------------------------------------+
    |Ethernet Segment Identifier (10 octets)|
    +---------------------------------------+
    |  Ethernet Tag ID (4 octets)           |
    +---------------------------------------+
    |  IP Prefix Length (1 octet)           |
    +---------------------------------------+
    |  IP Prefix (4 or 16 octets)           |
    +---------------------------------------+
    |  GW IP Address (4 or 16 octets)       |
    +---------------------------------------+
    |  MPLS Label (3 octets)                |
    +---------------------------------------+
    """
    @classmethod
    def parse(cls, value, iswithdraw=False):
        route = dict()
        offset = 8
        route['rd'] = cls.parse_rd(value[0:offset])
        # esi
        route['esi'] = int(binascii.b2a_hex(value[offset: offset+10]), 16)
        offset += 10

        route['eth_tag_id'] = struct.unpack('!I', value[offset: offset+4])[0]
        offset += 4

        ip_addr_len = ord(value[offset: offset + 1])
        offset += 1

        value = value[offset:]
        # The IP Prefix Length can be set to a value between 0 and 32
        #   (bits) for ipv4 and between 0 and 128 for ipv6.
        # The IP Prefix will be a 32 or 128-bit field (ipv4 or ipv6).

        # # ip address
        if len(value) == 11:
            # ipv4
            offset = 4
        elif len(value) == 35:
            # ipv6
            offset = 16

        route['prefix'] = '%s/%s' % (str(netaddr.IPAddress(int(binascii.b2a_hex(value[0: offset]), 16))), ip_addr_len)
        value = value[offset:]
        route['gateway'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value[0: offset]), 16)))
        value = value[offset:]

        route['label'] = cls.parse_mpls_label_stack(value)
        return route

    @classmethod
    def construct(cls, value, iswithdraw=False):
        value_hex = b''
        value_hex += cls.construct_rd(value['rd'])
        value_hex += b'\x00\x00' + struct.pack('!d', value['esi'])
        value_hex += struct.pack('!I', value['eth_tag_id'])
        value_hex += struct.pack('!B', int(value['prefix'].split('/')[1]))
        value_hex += netaddr.IPAddress(value['prefix'].split('/')[0]).packed
        value_hex += netaddr.IPAddress(value['gateway']).packed
        value_hex += cls.construct_mpls_label_stack(value['label'])
        return value_hex
