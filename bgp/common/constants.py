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

""" All BGP constant values """

# some handy things to know
BGP_MAX_PACKET_SIZE = 4096
BGP_MARKER_SIZE = 16  # size of BGP marker
BGP_HEADER_SIZE = 19  # size of BGP header, including marker
BGP_MIN_OPEN_MSG_SIZE = 29
BGP_MIN_UPDATE_MSG_SIZE = 23
BGP_MIN_NOTIFICATION_MSG_SIZE = 21
BGP_MIN_KEEPALVE_MSG_SIZE = BGP_HEADER_SIZE
BGP_TCP_PORT = 179
BGP_ROUTE_DISTINGUISHER_SIZE = 8

# BGP message types
BGP_OPEN = 1
BGP_UPDATE = 2
BGP_NOTIFICATION = 3
BGP_KEEPALIVE = 4
BGP_ROUTE_REFRESH = 5
BGP_CAPABILITY = 6
BGP_ROUTE_REFRESH_CISCO = 0x80

BGP_SIZE_OF_PATH_ATTRIBUTE = 2

# attribute flags, from RFC1771
BGP_ATTR_FLAG_OPTIONAL = 0x80
BGP_ATTR_FLAG_TRANSITIVE = 0x40
BGP_ATTR_FLAG_PARTIAL = 0x20
BGP_ATTR_FLAG_EXTENDED_LENGTH = 0x10


# SSA flags
BGP_SSA_TRANSITIVE = 0x8000
BGP_SSA_TYPE = 0x7FFF

# SSA Types
BGP_SSA_L2TPv3 = 1
BGP_SSA_mGRE = 2
BGP_SSA_IPSec = 3
BGP_SSA_MPLS = 4
BGP_SSA_L2TPv3_IN_IPSec = 5
BGP_SSA_mGRE_IN_IPSec = 6

# AS_PATH segment types
AS_SET = 1  # RFC1771
AS_SEQUENCE = 2  # RFC1771
AS_CONFED_SET = 4  # RFC1965 has the wrong values, corrected in
AS_CONFED_SEQUENCE = 3  # draft-ietf-idr-bgp-confed-rfc1965bis-01.txt

# OPEN message Optional Parameter types
BGP_OPTION_AUTHENTICATION = 1  # RFC1771
BGP_OPTION_CAPABILITY = 2  # RFC2842

# attribute types
BGPTYPE_ORIGIN = 1  # RFC1771
BGPTYPE_AS_PATH = 2  # RFC1771
BGPTYPE_NEXT_HOP = 3  # RFC1771
BGPTYPE_MULTI_EXIT_DISC = 4  # RFC1771
BGPTYPE_LOCAL_PREF = 5  # RFC1771
BGPTYPE_ATOMIC_AGGREGATE = 6  # RFC1771
BGPTYPE_AGGREGATOR = 7  # RFC1771
BGPTYPE_COMMUNITIES = 8  # RFC1997
BGPTYPE_ORIGINATOR_ID = 9  # RFC2796
BGPTYPE_CLUSTER_LIST = 10  # RFC2796
BGPTYPE_DPA = 11  # work in progress
BGPTYPE_ADVERTISER = 12  # RFC1863
BGPTYPE_RCID_PATH = 13  # RFC1863
BGPTYPE_MP_REACH_NLRI = 14  # RFC2858
BGPTYPE_MP_UNREACH_NLRI = 15  # RFC2858
BGPTYPE_EXTENDED_COMMUNITY = 16  # Draft Ramachandra
BGPTYPE_NEW_AS_PATH = 17  # draft-ietf-idr-as4bytes
BGPTYPE_NEW_AGGREGATOR = 18  # draft-ietf-idr-as4bytes
BGPTYPE_SAFI_SPECIFIC_ATTR = 19  # draft-kapoor-nalawade-idr-bgp-ssa-00.txt
BGPTYPE_PMSI_TUNNEL = 22  # RFC 6514
BGPTYPE_TUNNEL_ENCAPS_ATTR = 23  # RFC5512
BGPTYPE_LINK_STATE = 29
BGPTYPE_LARGE_COMMUNITY = 32
BGPTYPE_ATTRIBUTE_SET = 128

# BGP Tunnel Encapsulation Attribute Tunnel Types
BGP_TUNNEL_ENCAPS_RESERVED = 0
BGP_TUNNEL_ENCAPS_L2TPV3_OVER_IP = 1
BGP_TUNNEL_ENCAPS_GRE = 2
BGP_TUNNEL_ENCAPS_TRANSMIT_TUNNEL_ENDPOINT = 3
BGP_TUNNEL_ENCAPS_IPSEC_TUNNEL_MODE = 4
BGP_TUNNEL_ENCAPS_IP_IN_IP_TUNNEL_WITH_IPSEC = 5
BGP_TUNNEL_ENCAPS_MPLS_IN_IP_TUNNEL_WITH_IPSEC = 6
BGP_TUNNEL_ENCAPS_IP_IN_IP = 7
BGP_TUNNEL_ENCAPS_VXLAN = 8
BGP_TUNNEL_ENCAPS_NVGRE = 9
BGP_TUNNEL_ENCAPS_MPLS = 10
BGP_TUNNEL_ENCAPS_MPLS_IN_GRE = 11
BGP_TUNNEL_ENCAPS_VXLAN_GRE = 12
BGP_TUNNEL_ENCAPS_MPLS_IN_UDP = 13
BGP_TUNNEL_ENCAPS_IPV6_TUNNEL = 14
BGP_TUNNEL_ENCAPS_SR_TE_POLICY_TYPE = 15
BGP_TUNNEL_ENCAPS_BARE = 16

# Segment Sub-TLV type
BGP_SRTE_SEGMENT_SUBTLV_MPLS = 1
BGP_SRTE_SEGMENT_SUBTLV_IPV6 = 2
BGP_SRTE_SEGMENT_SUBTLV_IPV4_SID = 3
BGP_SRTE_SEGMENT_SUBTLV_IPV6_SID = 4
BGP_SRTE_SEGMENT_SUBTLV_IPV4_INDEX_SID = 5
BGP_SRTE_SEGMENT_SUBTLV_IPV4_ADDR_SID = 6
BGP_SRTE_SEGMENT_SUBTLV_IPV6_INDEX_SID = 7
BGP_SRTE_SEGMENT_SUBTLV_IPV6_ADDR_SID = 8

#  VPN Route Target  #
BGP_EXT_COM_RT_0 = 0x0002  # Route Target,Format AS(2bytes):AN(4bytes)
BGP_EXT_COM_RT_1 = 0x0102  # Route Target,Format IPv4 address(4bytes):AN(2bytes)
BGP_EXT_COM_RT_2 = 0x0202  # Route Target,Format AS(4bytes):AN(2bytes)

# Route Origin (SOO site of Origin)
BGP_EXT_COM_RO_0 = 0x0003  # Route Origin,Format AS(2bytes):AN(4bytes)
BGP_EXT_COM_RO_1 = 0x0103  # Route Origin,Format IP address:AN(2bytes)
BGP_EXT_COM_RO_2 = 0x0203  # Route Origin,Format AS(4bytes):AN(2bytes)

# BGP Flow Spec
BGP_EXT_REDIRECT_NH = 0x0800  # redirect to ipv4/v6 nexthop
BGP_EXT_TRA_RATE = 0x8006  # traffic-rate 2-byte as#, 4-byte float
BGP_EXT_TRA_ACTION = 0x8007  # traffic-action bitmask
BGP_EXT_REDIRECT_VRF = 0x8008  # redirect 6-byte Route Target
BGP_EXT_TRA_MARK = 0x8009  # traffic-marking DSCP value

# Transitive Opaque
BGP_EXT_COM_OSPF_ROUTE_TYPE = 0x0306  # OSPF Route Type
BGP_EXT_COM_COLOR = 0x030b  # Color
BGP_EXT_COM_COLOR_00 = 0x030b0000  # Color-00
BGP_EXT_COM_COLOR_01 = 0x030b4000  # Color-01
BGP_EXT_COM_COLOR_10 = 0x030b8000  # Color-10
BGP_EXT_COM_COLOR_11 = 0x030bc000  # Color-11
BGP_EXT_COM_ENCAP = 0x030c  # BGP_EXT_COM_ENCAP = 0x030c
BGP_EXT_COM_DEFAULT_GATEWAY = 0x030d  # Default Gateway

# BGP EVPN
BGP_EXT_COM_EVPN_MAC_MOBIL = 0x0600  # Mac Mobility
BGP_EXT_COM_EVPN_ESI_MPLS_LABEL = 0x0601  # ESI MPLS Label
BGP_EXT_COM_EVPN_ES_IMPORT = 0x0602  # ES Import
BGP_EXT_COM_EVPN_ROUTE_MAC = 0x0603  # EVPN Router MAC Extended Community

# BGP cost cummunity
BGP_EXT_COM_COST = 0x4301

# BGP link bandwith
BGP_EXT_COM_LINK_BW = 0x4004

# Unkonw
BGP_EXT_COM_UNKNOW = 0x0000

BGP_EXT_COM_DICT = {
    'redirect-vrf': 32776,  # redirect 6-byte Route Target
    'traffic-marking-dscp': 32777,  # traffic-marking DSCP value
    'traffic-rate': 32774,  # traffic-rate 2-byte as#, 4-byte float
    'color': 779,  # Color
    # Color, leftmost 2 bits of reserved field = 00, CO bits = 00,
    # srpolicy -> IGP
    'color-00': 51052544,
    # Color, leftmost 2 bits of reserved field = 01, CO bits = 01,
    # srpolicy -> same afi null endpoint -> any null endpoint -> IGP
    'color-01': 51068928,
    # Color, leftmost 2 bits of reserved field = 10, CO bits = 10,
    # srpolicy -> same afi null endpoint -> any null endpoint -> same afi endpoint -> any endpoint -> IGP
    'color-10': 51085312,
    # Color, leftmost 2 bits of reserved field = 11, CO bits = 11,
    # treated like color-00
    'color-11': 51101696,
    'encapsulation': 780,  # BGP_EXT_COM_ENCAP = 0x030c
    'es-import': 1538,  # ES Import
    'router-mac': 1539  # EVPN Router MAC Extended Community
}

BGP_EXT_COM_DICT_1 = {
    'esi-label': 1537,  # ESI MPLS Label
    'mac-mobility': 1536,  # Mac Mobility
}

# route distinguisher type
BGP_ROUTE_DISTINGUISHER_TYPE_0 = 0x0000
BGP_ROUTE_DISTINGUISHER_TYPE_1 = 0x0001
BGP_ROUTE_DISTINGUISHER_TYPE_2 = 0x0002

# PMSI TUNNEL TYPE
PMSI_TUNNEL_TYPE_NO_TUNNEL = 0
PMSI_TUNNEL_TYPE_RSVP_TE_P2MP = 1
PMSI_TUNNEL_TYPE_MLDP_P2MP = 2
PMSI_TUNNEL_TYPE_PIM_SSM_TREE = 3
PMSI_TUNNEL_TYPE_PIM_SM_TREE = 4
PMSI_TUNNEL_TYPE_BIDIR_PIM_TREE = 5
PMSI_TUNNEL_TYPE_INGRESS_REPL = 6
PMSI_TUNNEL_TYPE_MLDP_MP2MP = 7

# NLRI type as define in BGP flow spec RFC
BGPNLRI_FSPEC_DST_PFIX = 1  # RFC 5575
BGPNLRI_FSPEC_SRC_PFIX = 2  # RFC 5575
BGPNLRI_FSPEC_IP_PROTO = 3  # RFC 5575
BGPNLRI_FSPEC_PORT = 4  # RFC 5575
BGPNLRI_FSPEC_DST_PORT = 5  # RFC 5575
BGPNLRI_FSPEC_SRC_PORT = 6  # RFC 5575
BGPNLRI_FSPEC_ICMP_TP = 7  # RFC 5575
BGPNLRI_FSPEC_ICMP_CD = 8  # RFC 5575
BGPNLRI_FSPEC_TCP_FLAGS = 9  # RFC 5575
BGPNLRI_FSPEC_PCK_LEN = 10  # RFC 5575
BGPNLRI_FSPEC_DSCP = 11  # RFC 5575
BGPNLRI_FSPEC_FRAGMENT = 12  # RFC 5575

# Sub-TLVs as defined in SR TE Policy draft
BGP_BSID_PREFERENCE_OLD_OR_NEW = 0
BGPSUB_TLV_PREFERENCE = 6
BGPSUB_TLV_BINDGINGSID = 7
BGPSUB_TLV_PREFERENCE_NEW = 12
BGPSUB_TLV_BINDGINGSID_NEW = 13
BGPSUB_TLV_SIDLIST = 128

# Sub-TLVs as defined in SR TE Policy draft and used in BGPSUB_TLV_SIDLIST
BGPSUB_TLV_WEIGHTED = 9
BGPSUB_TLV_SID = 1

# NLRI type as define in BGP EVPN
BGPNLRI_EVPN_ETHERNET_AUTO_DISCOVERY = 1
BGPNLRI_EVPN_MAC_IP_ADVERTISEMENT = 2
BGPNLRI_EVPN_INCLUSIVE_MULTICAST_ETHERNET_TAG = 3
BGPNLRI_EVPN_ETHERNET_SEGMENT = 4
BGPNLRI_EVPN_IP_ROUTE_PREFIX = 5

# BGP message Constants
VERSION = 4
PORT = 179
HDR_LEN = 19
MAX_LEN = 4096

# BGP messages type
MSG_BGP_CLOSED = 0
MSG_OPEN = 1
MSG_UPDATE = 2
MSG_NOTIFICATION = 3
MSG_KEEPALIVE = 4
MSG_ROUTEREFRESH = 5
MSG_CISCOROUTEREFRESH = 128

# BGP Capabilities Support

SUPPORT_4AS = False
CISCO_ROUTE_REFRESH = False
NEW_ROUTE_REFRESH = False
GRACEFUL_RESTART = False

# AFI_SAFI mapping

AFI_SAFI_DICT = {
    (1, 1): 'ipv4',
    (2, 1): 'ipv6',
    (1, 4): 'ipv4_lu',
    (2, 4): 'ipv6_lu',
    (1, 133): 'flowspec',
    (1, 128): 'vpnv4',
    (2, 128): 'vpnv6',
    (25, 70): 'evpn',
    (16388, 71): 'bgpls',
    (1, 73): 'ipv4_srte'
}
AFI_SAFI_STR_DICT = {
    'ipv6': (2, 1),
    'ipv4': (1, 1),
    'ipv4_lu': (1, 4),
    'ipv6_lu': (2, 4),
    'flowspec': (1, 133),
    'vpnv4': (1, 128),
    'vpnv6': (2, 128),
    'evpn': (25, 70),
    'bgpls': (16388, 71),
    'ipv4_srte': (1, 73)
}

ADD_PATH_ACT_DICT = {
    1: 'receive',
    2: 'send',
    3: 'both'
}
# BGP FSM State
ST_IDLE = 1
ST_CONNECT = 2
ST_ACTIVE = 3
ST_OPENSENT = 4
ST_OPENCONFIRM = 5
ST_ESTABLISHED = 6

# BGP Timer (seconds)
# DELAY_OPEN_TIME = 10
ROUTE_REFRESH_TIME = 10
LARGER_HOLD_TIME = 4 * 60
# CONNECT_RETRY_TIME = 30
# IDLEHOLD_TIME = 30
# HOLD_TIME = 120

stateDescr = {
    ST_IDLE: "IDLE",
    ST_CONNECT: "CONNECT",
    ST_ACTIVE: "ACTIVE",
    ST_OPENSENT: "OPENSENT",
    ST_OPENCONFIRM: "OPENCONFIRM",
    ST_ESTABLISHED: "ESTABLISHED"
}

# Notification error codes
ERR_MSG_HDR = 1
ERR_MSG_OPEN = 2
ERR_MSG_UPDATE = 3
ERR_HOLD_TIMER_EXPIRED = 4
ERR_FSM = 5
ERR_CEASE = 6
ERR_CAP = 7

# Notification error codes dict
NOTIFICATION_ERROR_CODES_DICT = {
    ERR_MSG_HDR: "Message Header Error",
    ERR_MSG_OPEN: "OPEN Message Error",
    ERR_MSG_UPDATE: "UPDATE Message Error",
    ERR_HOLD_TIMER_EXPIRED: "Hold Timer Expired",
    ERR_FSM: "Finite State Machine Error",
    ERR_CEASE: "Cease",
    ERR_CAP: "CAPABILITY Message Error"
}

# Notification suberror codes for ERR_MSG_HDR
ERR_MSG_HDR_CONN_NOT_SYNC = 1
ERR_MSG_HDR_BAD_MSG_LEN = 2
ERR_MSG_HDR_BAD_MSG_TYPE = 3

# Notification suberror codes for ERR_MSG_OPEN
ERR_MSG_OPEN_UNSUP_VERSION = 1
ERR_MSG_OPEN_BAD_PEER_AS = 2
ERR_MSG_OPEN_BAD_BGP_ID = 3
ERR_MSG_OPEN_UNSUP_OPT_PARAM = 4
ERR_MSG_OPEN_UNACCPT_HOLD_TIME = 6
ERR_MSG_OPEN_UNSUP_CAPA = 7  # RFC 5492
ERR_MSG_OPEN_UNKNO = 8

# Notification suberror codes for ERR_MSG_UPDATE
ERR_MSG_UPDATE_MALFORMED_ATTR_LIST = 1
ERR_MSG_UPDATE_UNRECOGNIZED_WELLKNOWN_ATTR = 2
ERR_MSG_UPDATE_MISSING_WELLKNOWN_ATTR = 3
ERR_MSG_UPDATE_ATTR_FLAGS = 4
ERR_MSG_UPDATE_ATTR_LEN = 5
ERR_MSG_UPDATE_INVALID_ORIGIN = 6
ERR_MSG_UPDATE_INVALID_NEXTHOP = 8
ERR_MSG_UPDATE_OPTIONAL_ATTR = 9
ERR_MSG_UPDATE_INVALID_NETWORK_FIELD = 10
ERR_MSG_UPDATE_MALFORMED_ASPATH = 11
ERR_MSG_UPDATE_UNKOWN_ATTR = 12

# Notification suberror codes for ERR_HOLD_TIMER_EXPIRED
ERR_SUB_HOLD_TIMER_EXPIRED = 1

# Notification suberror codes for ERR_FSM
ERR_SUB_FSM_ERROR = 1

# Notification suberror codes for ERR_CEASE
ERR_MAXIMUM_NUMBER_OF_PREFIXES_REACHED = 1
ERR_ADMINISTRATIVE_SHUTDOWN = 2
ERR_PEER_DECONFIGURED = 3
ERR_ADMINISTRATIVE_RESET = 4
ERR_CONNECTION_RESET = 5
ERR_OTHER_CONFIGURATION_CHANGE = 6
ERR_CONNECTION_COLLISION_RESOLUTION = 7
ERR_OUT_OF_RESOURCES = 8

NOTIFICATION_SUB_ERROR_CODES_DICT = {
    ERR_MSG_HDR: {
        ERR_MSG_HDR_CONN_NOT_SYNC: 'Connection Not Synchronized',  # 1
        ERR_MSG_HDR_BAD_MSG_LEN: 'Bad Message Length',             # 2
        ERR_MSG_HDR_BAD_MSG_TYPE: 'Bad Message Type'               # 3
    },
    ERR_MSG_OPEN: {
        ERR_MSG_OPEN_UNSUP_VERSION: 'Unsupported Version Number',
        ERR_MSG_OPEN_BAD_PEER_AS: 'Bad Peer AS',
        ERR_MSG_OPEN_BAD_BGP_ID: 'Bad BGP Identifier',
        ERR_MSG_OPEN_UNSUP_OPT_PARAM: 'Unsupported Optional Parameter',
        ERR_MSG_OPEN_UNACCPT_HOLD_TIME: 'Unacceptable Hold Time',
        ERR_MSG_OPEN_UNSUP_CAPA: 'Unsupported Capability',
        ERR_MSG_OPEN_UNKNO: 'NULL',
    },
    ERR_MSG_UPDATE: {
        ERR_MSG_UPDATE_MALFORMED_ATTR_LIST: 'Malformed Attribute List',
        ERR_MSG_UPDATE_UNRECOGNIZED_WELLKNOWN_ATTR: 'Unrecognized Well-known Attribute',
        ERR_MSG_UPDATE_MISSING_WELLKNOWN_ATTR: 'Missing Well-known Attribute',
        ERR_MSG_UPDATE_ATTR_FLAGS: 'Attribute Flags Error',
        ERR_MSG_UPDATE_ATTR_LEN: 'Attribute Length Error',
        ERR_MSG_UPDATE_INVALID_ORIGIN: 'Invalid ORIGIN Attribute',
        ERR_MSG_UPDATE_INVALID_NEXTHOP: 'Invalid NEXT_HOP Attribute',
        ERR_MSG_UPDATE_OPTIONAL_ATTR: 'Optional Attribute Error',
        ERR_MSG_UPDATE_INVALID_NETWORK_FIELD: 'Invalid Network Field',
        ERR_MSG_UPDATE_MALFORMED_ASPATH: 'Malformed AS_PATH',
        ERR_MSG_UPDATE_UNKOWN_ATTR: 'NULL'
    },
    ERR_HOLD_TIMER_EXPIRED: {
        ERR_SUB_HOLD_TIMER_EXPIRED: 'Hold timer expired'
    },
    ERR_FSM: {
        ERR_SUB_FSM_ERROR: 'FSM error'
    },
    ERR_CEASE: {
        ERR_MAXIMUM_NUMBER_OF_PREFIXES_REACHED: 'Maximum number of prefixes reached',
        ERR_ADMINISTRATIVE_SHUTDOWN: 'Administrative shutdown',
        ERR_PEER_DECONFIGURED: 'Peer reconfigured',
        ERR_ADMINISTRATIVE_RESET: 'Administrative reset',
        ERR_CONNECTION_RESET: 'Connection reset',
        ERR_OTHER_CONFIGURATION_CHANGE: 'Other configuration change',
        ERR_CONNECTION_COLLISION_RESOLUTION: 'Connection collision resolution',
        ERR_OUT_OF_RESOURCES: 'Out of resources'
    }
}

ATTRIBUTE_ID_2_STR = {
    1: 'ORIGIN',
    2: 'AS_PATH',
    3: 'NEXT_HOP',
    4: 'MULTI_EXIT_DISC',
    5: 'LOCAL_PREF',
    6: 'ATOMIC_AGGREGATE',
    7: 'AGGREGATOR',
    8: 'COMMUNITY',
    9: 'ORIGINATOR_ID',
    10: 'CLUSTER_LIST',
    14: 'MP_REACH_NLRI',
    15: 'MP_UNREACH_NLRI',
    16: 'EXTENDED_COMMUNITY',
    17: 'AS4_PATH',
    18: 'AS4_AGGREGATOR',
    22: 'PMSI_TUNNEL'
}

ATTRIBUTE_STR_2_ID = dict([(v, k) for (k, v) in ATTRIBUTE_ID_2_STR.items()])


WELL_KNOW_COMMUNITY_INT_2_STR = {
    0xFFFF0000: 'PLANNED_SHUT',
    0xFFFF0001: 'ACCEPT_OWN',
    0xFFFF0002: 'ROUTE_FILTER_TRANSLATED_v4',
    0xFFFF0003: 'ROUTE_FILTER_v4',
    0xFFFF0004: 'ROUTE_FILTER_TRANSLATED_v6',
    0xFFFF0005: 'ROUTE_FILTER_v6',
    0xFFFF029A: 'BLACKHOLE',
    0xFFFFFF01: 'NO_EXPORT',
    0xFFFFFF02: 'NO_ADVERTISE',
    0xFFFFFF03: 'NO_EXPORT_SUBCONFED',
    0xFFFFFF04: 'NOPEER'
}

WELL_KNOW_COMMUNITY_STR_2_INT = dict(
    [(r, l) for (l, r) in WELL_KNOW_COMMUNITY_INT_2_STR.items()])

TCP_MD5SIG_MAXKEYLEN = 80
SS_PADSIZE_IPV4 = 120
TCP_MD5SIG = 14
SS_PADSIZE_IPV6 = 100
SIN6_FLOWINFO = 0
SIN6_SCOPE_ID = 0
