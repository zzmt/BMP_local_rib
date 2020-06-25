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
"""linkstate
"""

from __future__ import division
import struct
import binascii

import netaddr

from bgp.message.attribute.nlri import NLRI


class BGPLS(NLRI):
    """BGPLS
    """
    NODE_NLRI = 1
    LINK_NLRI = 2
    IPv4_TOPO_PREFIX_NLRI = 3
    IPv6_TOPO_PREFIX_NLRI = 4

    @classmethod
    def parse(cls, nlri_data):
        nlri_list = []
        while nlri_data:
            _type, length = struct.unpack('!HH', nlri_data[0:4])
            value = nlri_data[4: 4 + length]
            nlri_data = nlri_data[4+length:]
            nlri = dict()
            if _type == cls.LINK_NLRI:
                nlri['type'] = 'link'
            elif _type == cls.NODE_NLRI:
                nlri['type'] = 'node'
            elif _type == cls.IPv4_TOPO_PREFIX_NLRI:
                nlri['type'] = 'ipv4_topo_prefix'
            elif _type == cls.IPv6_TOPO_PREFIX_NLRI:
                nlri['type'] = 'ipv6_topo_prefix'
            else:
                nlri['type'] = 'unknown'
                continue
            protocol_id, identifier, descriptors = cls.parse_nlri(value, _type)
            nlri['protocol_id'] = protocol_id
            nlri['instances_id'] = identifier
            nlri['descriptors'] = descriptors
            nlri_list.append(nlri)
        return nlri_list

    @classmethod
    def parse_nlri(cls, data, nlri_type):
        """parse nlri: node, link, prefix
        """
        #      0                   1                   2                   3
        #      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        #     +-+-+-+-+-+-+-+-+
        #     |  Protocol-ID  |
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     |                           Identifier                          |
        #     |                            (64 bits)                          |
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     //               Local Node Descriptors (variable)             //
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     //               Remote Node Descriptors (variable)            //
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     //                  Link Descriptors (variable)                //
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #                     Figure 8: The Link NLRI format

        # The Protocol-ID field can contain one of the following values:
        #     +-------------+----------------------------------+
        #     | Protocol-ID | NLRI information source protocol |
        #     +-------------+----------------------------------+
        #     |      1      | IS-IS Level 1                    |
        #     |      2      | IS-IS Level 2                    |
        #     |      3      | OSPFv2                           |
        #     |      4      | Direct                           |
        #     |      5      | Static configuration             |
        #     |      6      | OSPFv3                           |
        #     |      7      | BGP                              |
        #     +-------------+----------------------------------+
        #               Table 2: Protocol Identifiers

        #     +------------+----------------------------------+
        #     | Identifier | Routing Universe                 |
        #     +------------+----------------------------------+
        #     |     0      | Default Layer 3 Routing topology |
        #     +------------+----------------------------------+
        #         Table 3: Well-Known Instance Identifiers

        proto_id = ord(data[0:1])

        identifier = int(binascii.b2a_hex(data[1:9]), 16)

        descriptor_list = []
        descriptors = data[9:]
        while descriptors:
            _type, length = struct.unpack('!HH', descriptors[0:4])
            value = descriptors[4: 4+length]
            descriptors = descriptors[4+length:]
            descriptor = dict()
            if _type == 256:  # local node
                descriptor['type'] = 'local_node'
                descriptor['value'] = cls.parse_node_descriptor(value, proto_id)

            elif _type == 257:  # remote node
                descriptor['type'] = 'remote_node'
                descriptor['value'] = cls.parse_node_descriptor(value, proto_id)
            # elif _type == 258:  # link local/remote identifier
            #     pass
            elif _type == 259:  # ipv4 interface address
                ipv4_addr = str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
                descriptor['type'] = 'link_local_ipv4'
                descriptor['value'] = ipv4_addr
            elif _type == 260:  # ipv4 neighbor address
                ipv4_neighbor_addr = str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
                descriptor['type'] = 'link_remote_ipv4'
                descriptor['value'] = ipv4_neighbor_addr
            # elif _type == 263: # Multi-Topology Identifier
            #     pass
            elif _type == 263:  # Multi-Topology Identifier
                descriptor['type'] = 'mt_id'
                descriptor['value'] = []
                while value:
                    descriptor['value'].append(struct.unpack('!H', value[:2])[0])
                    value = value[2:]
            elif _type == 264:  # OSPF Route Type
                descriptor['type'] = 'prefix_ospf_route_type'
                descriptor['value'] = ord(value[0:1])
            elif _type == 265:   # IP Reachability Information
                descriptor['type'] = 'prefix'
                mask = ord(value[0:1])
                if nlri_type == cls.IPv4_TOPO_PREFIX_NLRI:
                    prefix_value = value[1:] + b'\x00' * (4 - len(value[1:]))
                    ip_str = str(netaddr.IPAddress(int(binascii.b2a_hex(prefix_value), 16)))
                else:
                    ip_str = str(netaddr.IPAddress(int(binascii.b2a_hex(value[1:]), 16)))
                descriptor['value'] = "%s/%s" % (ip_str, mask)
            else:
                descriptor['type'] = _type
                descriptor['value'] = binascii.b2a_hex(value)
            descriptor_list.append(descriptor)
        return proto_id, identifier, descriptor_list

    @classmethod
    def parse_node_descriptor(cls, data, proto):

        # +--------------------+-------------------+----------+
        # | Sub-TLV Code Point | Description       |   Length |
        # +--------------------+-------------------+----------+
        # |        512         | Autonomous System |        4 |
        # |        513         | BGP-LS Identifier |        4 |
        # |        514         | OSPF Area-ID      |        4 |
        # |        515         | IGP Router-ID     | Variable |
        # |        516         | BGP Router-ID     |        4 |
        # |        517         | Member-ASN        |        4 |
        # +--------------------+-------------------+----------+
        return_data = dict()
        while data:
            _type, length = struct.unpack('!HH', data[0: 4])
            value = data[4: 4+length]
            data = data[4+length:]
            if _type == 512:
                return_data['as_num'] = int(binascii.b2a_hex(value), 16)
            elif _type == 513:
                return_data['bgpls_id'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
            elif _type == 514:
                return_data['ospf_area_id'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
            elif _type == 515:
                # OSPFv2, OSPFv3 non-pseudonode
                if (proto == 3 or proto == 6) and length == 4:
                    return_data['igp_router_id'] = {
                        "pseudonode": False,
                        "router_id": str(netaddr.IPAddress(int(binascii.b2a_hex(value), 16)))
                    }
                # OSPFv2, OSPFv3, LAN pseudonode
                if (proto == 3 or proto == 6) and length == 8:
                    return_data['igp_router_id'] = {
                        "pseudonode": True,
                        "router_id": str(netaddr.IPAddress(int(binascii.b2a_hex(value[:4]), 16))),
                        "designated_router_addr": str(netaddr.IPAddress(int(binascii.b2a_hex(value[4:]), 16)))
                    }
                # IS-IS non-pseudonode
                if (proto == 1 or proto == 2) and length == 6:
                    return_data['igp_router_id'] = {
                        "pseudonode": False,
                        "iso_node_id": cls.parse_iso_node_id(value)
                    }
                # IS-IS LAN pseudonode = ISO Node-ID + PSN
                # Unpack ISO address
                if (proto == 1 or proto == 2) and length == 7:
                    return_data['igp_router_id'] = {
                        "pseudonode": True,
                        "psn": ord(value[6: 7]),
                        "iso_node_id": cls.parse_iso_node_id(value[:6])
                    }
            elif _type == 516:
                return_data['bgp_router_id'] = str(netaddr.IPAddress(int(binascii.b2a_hex(value[:4]), 16)))
            elif _type == 517:
                return_data['member_as_num'] = int(binascii.b2a_hex(value), 16)
        return return_data

    @classmethod
    def parse_iso_node_id(cls, data):
        tmp = binascii.b2a_hex(data).decode('utf-8')
        chunks, chunk_size = len(tmp), len(tmp) // 3
        return '.'.join([str(tmp[i:i+chunk_size]) for i in range(0, chunks, chunk_size)])
