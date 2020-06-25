# Copyright 2015-2017 Cisco Systems, Inc.
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

"""BGP Update Message"""

import struct
import traceback
import logging
import binascii

import netaddr

from bgp.common import exception as excep
from bgp.common import constants as bgp_cons
from bgp.message.attribute import AttributeFlag
from bgp.message.attribute.origin import Origin
from bgp.message.attribute.aspath import ASPath
from bgp.message.attribute.nexthop import NextHop
from bgp.message.attribute.med import MED
from bgp.message.attribute.localpref import LocalPreference
from bgp.message.attribute.atomicaggregate import AtomicAggregate
from bgp.message.attribute.aggregator import Aggregator
from bgp.message.attribute.community import Community
from bgp.message.attribute.originatorid import OriginatorID
from bgp.message.attribute.clusterlist import ClusterList
from bgp.message.attribute.mpreachnlri import MpReachNLRI
from bgp.message.attribute.mpunreachnlri import MpUnReachNLRI
from bgp.message.attribute.tunnelencaps import TunnelEncaps
from bgp.message.attribute.extcommunity import ExtCommunity
from bgp.message.attribute.pmsitunnel import PMSITunnel
from bgp.message.attribute.linkstate.linkstate import LinkState
from bgp.message.attribute.nlri.evpn import EVPN
from bgp.message.attribute.largecommunity import LargeCommunity

LOG = logging.getLogger()


class Update(object):
    """
    An UPDATE message is used to advertise feasible routes that share
    common path attributes to a peer, or to withdraw multiple unfeasible
    routes from service (RFC 4271 page 15)
    """

    def __init__(self):
        """
        +----------------------------------------------------+
        |     Withdrawn Routes Length (2 octets)             |
        +----------------------------------------------------+
        |     Withdrawn Routes (variable)                    |
        +----------------------------------------------------+
        |     Total Path Attribute Length (2 octets)         |
        +----------------------------------------------------+
        |     Path Attributes (variable)                     |
        +----------------------------------------------------+
        |  Network Layer Reachability Information (variable) |
        +----------------------------------------------------+

        @ Withdrawn Routes Length:
            This 2-octets unsigned integer indicates the total length of
        the Withdrawn Routes field in octets. Its value allows the
        length of the Network Layer Reachability Information field to
        be determined, as specified below.
            A value of 0 indicates that no routes are being withdrawn from
        service, and that the WITHDRAWN ROUTES field is not present in
        this UPDATE message.

        @ Withdrawn Routes:
            This is a variable-length field that contains a list of IP
        address prefixes for the routes that are being withdrawn from
        service. Each IP address prefix is encoded as a 2-tuple of the
        form <length, prefix>, whose fields are described below:
                    +---------------------------+
                    |     Length (1 octet)      |
                    +---------------------------+
                    |     Prefix (variable)     |
                    +---------------------------+
            The use and the meaning of these fields are as follows:
            a) Length:
            The Length field indicates the length in bits of the IP
            address prefix. A length of zero indicates a prefix that
            matches all IP addresses (with prefix, itself, of zero
            octets).
            b) Prefix:
            The Prefix field contains an IP address prefix, followed by
            the minimum number of trailing bits needed to make the end
            of the field fall on an octet boundary. Note that the value
            of trailing bits is irrelevant.

        @ Total Path Attribute Length:
            This 2-octet unsigned integer indicates the total length of the
        Path Attributes field in octets. Its value allows the length
        of the Network Layer Reachability field to be determined as
        specified below.
            A value of 0 indicates that neither the Network Layer
        Reachability Information field nor the Path Attribute field is
        present in this UPDATE message.

        @ Path Attributes:
            (path attributes details see RFC 4271 and some other RFCs)

        @ Network Layer Reachability Information:
            This variable length field contains a list of IP address
        prefixes. The length, in octets, of the Network Layer
        Reachability Information is not encoded explicitly, but can be
        calculated as:
        UPDATE message Length - 23 - Total Path Attributes Length
        - Withdrawn Routes Length
        where UPDATE message Length is the value encoded in the fixedsize
        BGP header, Total Path Attribute Length, and Withdrawn
        Routes Length are the values encoded in the variable part of
        the UPDATE message, and 23 is a combined length of the fixedsize
        BGP header, the Total Path Attribute Length field, and the
        Withdrawn Routes Length field.
        Reachability information is encoded as one or more 2-tuples of
        the form <length, prefix>, whose fields are described below:
                    +---------------------------+
                    |      Length (1 octet)     |
                    +---------------------------+
                    |      Prefix (variable)    |
                    +---------------------------+
        The use and the meaning of these fields are as follows:
            a) Length:
                The Length field indicates the length in bits of the IP
            address prefix. A length of zero indicates a prefix that
            matches all IP addresses (with prefix, itself, of zero
            octets).
            b) Prefix:
                The Prefix field contains an IP address prefix, followed by
            enough trailing bits to make the end of the field fall on an
            octet boundary. Note that the value of the trailing bits is
            irrelevant.
        """

    @classmethod
    def parse(cls, t, msg_hex, asn4=False, add_path_remote=False, add_path_local=False):

        """
        Parse BGP Update message
        :param t: timestamp
        :param msg_hex: raw message
        :param asn4: support 4 bytes AS or not
        :param add_path_remote: if the remote peer can send add path NLRI
        :param add_path_local: if the local can send add path NLRI
        :return: message after parsing.
        """
        results = {
            "withdraw": [],
            "attr": None,
            "nlri": [],
            'time': t,
            'hex': msg_hex,
            'sub_error': None,
            'err_data': None}

        # get every part of the update message
        withdraw_len = struct.unpack('!H', msg_hex[:2])[0]
        withdraw_prefix_data = msg_hex[2:withdraw_len + 2]
        attr_len = struct.unpack('!H', msg_hex[withdraw_len + 2:withdraw_len + 4])[0]
        attribute_data = msg_hex[withdraw_len + 4:withdraw_len + 4 + attr_len]
        nlri_data = msg_hex[withdraw_len + 4 + attr_len:]
        try:
            # parse withdraw prefixes
            results['withdraw'] = cls.parse_prefix_list(withdraw_prefix_data, add_path_remote)

            # parse nlri
            results['nlri'] = cls.parse_prefix_list(nlri_data, add_path_remote)
        except Exception as e:
            LOG.error(e)
            error_str = traceback.format_exc()
            LOG.debug(error_str)
            results['sub_error'] = bgp_cons.ERR_MSG_UPDATE_INVALID_NETWORK_FIELD
            results['err_data'] = ''
        try:
            # parse attributes
            results['attr'] = cls.parse_attributes(attribute_data, asn4)
        except excep.UpdateMessageError as e:
            LOG.error(e)
            results['sub_error'] = e.sub_error
            results['err_data'] = e.data
        except Exception as e:
            LOG.error(e)
            error_str = traceback.format_exc()
            LOG.debug(error_str)
            results['sub_error'] = e
            results['err_data'] = e

        return results

    @classmethod
    def construct(cls, msg_dict, asn4=False, addpath=False):
        """construct BGP update message

        :param msg_dict: update message string
        :param asn4: support 4 bytes asn or not
        :param addpath: support add path or not
        """
        attr_hex = b''
        nlri_hex = b''
        withdraw_hex = b''
        if msg_dict.get('attr'):
            attr_hex = cls.construct_attributes(msg_dict['attr'], asn4)
        if msg_dict.get('nlri'):
            nlri_hex = cls.construct_prefix_v4(msg_dict['nlri'], addpath)
        if msg_dict.get('withdraw'):
            withdraw_hex = cls.construct_prefix_v4(msg_dict['withdraw'], addpath)
        if nlri_hex and attr_hex:
            msg_body = struct.pack('!H', 0) + struct.pack('!H', len(attr_hex)) + attr_hex + nlri_hex
            return cls.construct_header(msg_body)
        elif attr_hex and not nlri_hex:
            msg_body = struct.pack('!H', 0) + struct.pack('!H', len(attr_hex)) + attr_hex + nlri_hex
            return cls.construct_header(msg_body)
        elif withdraw_hex:
            msg_body = struct.pack('!H', len(withdraw_hex)) + withdraw_hex + struct.pack('!H', 0)
            return cls.construct_header(msg_body)

    @staticmethod
    def parse_prefix_list(data, addpath=False):
        """
        Parses an RFC4271 encoded blob of BGP prefixes into a list

        :param data: hex data
        :param addpath: support addpath or not
        :return: prefix_list
        """
        prefixes = []
        postfix = data
        while len(postfix) > 0:
            # for python2 and python3
            if addpath:
                path_id = struct.unpack('!I', postfix[0:4])[0]
                postfix = postfix[4:]
            if isinstance(postfix[0], int):
                prefix_len = postfix[0]
            else:
                prefix_len = ord(postfix[0])
            if prefix_len > 32:
                LOG.warning('Prefix Length larger than 32')
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_INVALID_NETWORK_FIELD,
                    data=repr(data)
                )
            octet_len, remainder = int(prefix_len / 8), prefix_len % 8
            if remainder > 0:
                # prefix length doesn't fall on octet boundary
                octet_len += 1
            tmp = postfix[1:octet_len + 1]
            # for python2 and python3
            if isinstance(postfix[0], int):
                prefix_data = [i for i in tmp]
            else:
                prefix_data = [ord(i) for i in tmp]
            # Zero the remaining bits in the last octet if it didn't fall
            # on an octet boundary
            if remainder > 0:
                prefix_data[-1] &= 255 << (8 - remainder)
            prefix_data = prefix_data + list(str(0)) * 4
            prefix = "%s.%s.%s.%s" % (tuple(prefix_data[0:4])) + '/' + str(prefix_len)
            if not addpath:
                prefixes.append(prefix)
            else:
                prefixes.append({'prefix': prefix, 'path_id': path_id})
            # Next prefix
            postfix = postfix[octet_len + 1:]

        return prefixes

    @staticmethod
    def parse_attributes(data, asn4=False):
        """
        Parses an RFC4271 encoded blob of BGP attributes into a list

        :param data:
        :param asn4: support 4 bytes asn or not
        :return:
        """
        attributes = {}
        postfix = data
        bgpls_pro_id = None
        bgpls_attr = None
        while len(postfix) > 0:

            try:
                flags, type_code = struct.unpack('!BB', postfix[:2])

                if flags & AttributeFlag.EXTENDED_LENGTH:
                    attr_len = struct.unpack('!H', postfix[2:4])[0]
                    attr_value = postfix[4:4 + attr_len]
                    postfix = postfix[4 + attr_len:]    # Next attribute
                else:    # standard 1-octet length
                    if isinstance(postfix[2], int):
                        attr_len = postfix[2]
                    else:
                        attr_len = ord(postfix[2])
                    attr_value = postfix[3:3 + attr_len]
                    postfix = postfix[3 + attr_len:]    # Next attribute
            except Exception as e:
                LOG.error(e)
                error_str = traceback.format_exc()
                LOG.debug(error_str)
                raise excep.UpdateMessageError(
                    sub_error=bgp_cons.ERR_MSG_UPDATE_MALFORMED_ATTR_LIST,
                    data='')

            if type_code == bgp_cons.BGPTYPE_ORIGIN:

                decode_value = Origin.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_AS_PATH:

                decode_value = ASPath.parse(value=attr_value, asn4=asn4)

            elif type_code == bgp_cons.BGPTYPE_NEXT_HOP:

                decode_value = NextHop.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_MULTI_EXIT_DISC:

                decode_value = MED.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_LOCAL_PREF:

                decode_value = LocalPreference.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_ATOMIC_AGGREGATE:

                decode_value = AtomicAggregate.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_AGGREGATOR:

                decode_value = Aggregator.parse(value=attr_value, asn4=asn4)

            elif type_code == bgp_cons.BGPTYPE_COMMUNITIES:

                decode_value = Community.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_ORIGINATOR_ID:

                decode_value = OriginatorID.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_CLUSTER_LIST:

                decode_value = ClusterList.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_NEW_AS_PATH:

                decode_value = ASPath.parse(value=attr_value, asn4=True)

            elif type_code == bgp_cons.BGPTYPE_NEW_AGGREGATOR:

                decode_value = Aggregator.parse(value=attr_value, asn4=True)

            elif type_code == bgp_cons.BGPTYPE_LARGE_COMMUNITY:

                decode_value = LargeCommunity.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_MP_REACH_NLRI:
                decode_value = MpReachNLRI.parse(value=attr_value)
                if decode_value['nlri'][0] and type(decode_value['nlri'][0]) is dict:
                    if decode_value['nlri'][0].get("protocol_id"):
                        bgpls_pro_id = decode_value['nlri'][0]["protocol_id"]

            elif type_code == bgp_cons.BGPTYPE_MP_UNREACH_NLRI:
                decode_value = MpUnReachNLRI.parse(value=attr_value)

            elif type_code == bgp_cons.BGPTYPE_EXTENDED_COMMUNITY:
                decode_value = ExtCommunity.parse(value=attr_value)
            elif type_code == bgp_cons.BGPTYPE_PMSI_TUNNEL:
                decode_value = PMSITunnel.parse(value=attr_value)
                pmsi_hex = attr_value
            elif type_code == bgp_cons.BGPTYPE_LINK_STATE:
                if bgpls_pro_id:
                    attributes.update(LinkState.unpack(bgpls_pro_id=bgpls_pro_id, data=attr_value).dict())
                else:
                    bgpls_attr = attr_value
                continue
            else:
                decode_value = binascii.b2a_hex(attr_value)
            attributes[type_code] = decode_value
        if bgpls_attr:
            attributes.update(LinkState.unpack(bgpls_pro_id=bgpls_pro_id, data=attr_value).dict())
        evpn_overlay = EVPN.signal_evpn_overlay(attributes)
        if evpn_overlay['evpn'] and evpn_overlay['encap_ec']:
            if bgp_cons.BGPTYPE_PMSI_TUNNEL in attributes:
                attributes[bgp_cons.BGPTYPE_PMSI_TUNNEL] = PMSITunnel.parse(value=pmsi_hex, evpn_overlay=evpn_overlay)
        return attributes

    @staticmethod
    def construct_attributes(attr_dict, asn4=False):

        """
        construts BGP Update attirubte.

        :param attr_dict: bgp attribute dictionary
        :param asn4: support 4 bytes asn or not
        """
        attr_raw_hex = b''
        for type_code, value in attr_dict.items():
            if type_code == bgp_cons.BGPTYPE_ORIGIN:
                origin_hex = Origin.construct(value=value)
                attr_raw_hex += origin_hex

            elif type_code == bgp_cons.BGPTYPE_AS_PATH:
                aspath_hex = ASPath.construct(value=value, asn4=asn4)
                attr_raw_hex += aspath_hex

            elif type_code == bgp_cons.BGPTYPE_NEXT_HOP:
                nexthop_hex = NextHop.construct(value=value)
                attr_raw_hex += nexthop_hex

            elif type_code == bgp_cons.BGPTYPE_MULTI_EXIT_DISC:
                med_hex = MED.construct(value=value)
                attr_raw_hex += med_hex

            elif type_code == bgp_cons.BGPTYPE_LOCAL_PREF:
                localpre_hex = LocalPreference.construct(value=value)
                attr_raw_hex += localpre_hex

            elif type_code == bgp_cons.BGPTYPE_ATOMIC_AGGREGATE:
                atomicaggregate_hex = AtomicAggregate.construct(value=value)
                attr_raw_hex += atomicaggregate_hex

            elif type_code == bgp_cons.BGPTYPE_AGGREGATOR:
                aggregator_hex = Aggregator.construct(value=value, asn4=asn4)
                attr_raw_hex += aggregator_hex

            elif type_code == bgp_cons.BGPTYPE_COMMUNITIES:
                community_hex = Community.construct(value=value)
                attr_raw_hex += community_hex

            elif type_code == bgp_cons.BGPTYPE_ORIGINATOR_ID:
                originatorid_hex = OriginatorID.construct(value=value)
                attr_raw_hex += originatorid_hex

            elif type_code == bgp_cons.BGPTYPE_CLUSTER_LIST:
                clusterlist_hex = ClusterList.construct(value=value)
                attr_raw_hex += clusterlist_hex

            elif type_code == bgp_cons.BGPTYPE_MP_REACH_NLRI:
                mpreach_hex = MpReachNLRI().construct(value=value)
                attr_raw_hex += mpreach_hex
            elif type_code == bgp_cons.BGPTYPE_MP_UNREACH_NLRI:
                mpunreach_hex = MpUnReachNLRI.construct(value=value)
                attr_raw_hex += mpunreach_hex
            elif type_code == bgp_cons.BGPTYPE_EXTENDED_COMMUNITY:
                community_ext_hex = ExtCommunity.construct(value=value)
                attr_raw_hex += community_ext_hex
            elif type_code == bgp_cons.BGPTYPE_PMSI_TUNNEL:
                evpn_overlay = EVPN.signal_evpn_overlay(attr_dict)
                attr_raw_hex += PMSITunnel.construct(value=value, evpn_overlay=evpn_overlay)
            elif type_code == bgp_cons.BGPTYPE_TUNNEL_ENCAPS_ATTR:
                tunnelencap_hex = TunnelEncaps.construct(value=value)
                attr_raw_hex += tunnelencap_hex
            elif type_code == bgp_cons.BGPTYPE_LARGE_COMMUNITY:
                large_community_ext_hex = LargeCommunity.construct(value=value)
                attr_raw_hex += large_community_ext_hex

        return attr_raw_hex

    @staticmethod
    def construct_header(msg):
        """
        Prepends the mandatory header to a constructed BGP message

        :param msg:
        :return:
        """
        #    16-octet     2-octet  1-octet
        # ---------------+--------+---------+------+
        #    Maker      | Length |  Type   |  msg |
        # ---------------+--------+---------+------+
        return b'\xff'*16 + struct.pack('!HB', len(msg) + 19, 2) + msg

    @staticmethod
    def construct_prefix_v4(prefix_list, add_path=False):
        """
        constructs NLRI prefix list

        :param prefix_list: prefix list
        :param add_path: support add path or not
        """
        nlri_raw_hex = b''
        for prefix in prefix_list:
            if add_path and isinstance(prefix, dict):
                path_id = prefix.get('path_id')
                prefix = prefix.get('prefix')
                nlri_raw_hex += struct.pack('!I', path_id)
            masklen = prefix.split('/')[1]
            ip_hex = struct.pack('!I', netaddr.IPNetwork(prefix).value)
            masklen = int(masklen)
            if 16 < masklen <= 24:
                ip_hex = ip_hex[0:3]
            elif 8 < masklen <= 16:
                ip_hex = ip_hex[0:2]
            elif masklen <= 8:
                ip_hex = ip_hex[0:1]
            nlri_raw_hex += struct.pack('!B', masklen) + ip_hex
        return nlri_raw_hex
