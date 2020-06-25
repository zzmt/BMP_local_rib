# Copyright 2015-2018 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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
import binascii

import netaddr

from bgp.message.attribute.linkstate.linkstate import LinkState
from bgp.tlv import TLV

# https://tools.ietf.org/html/draft-gredler-idr-bgp-ls-segment-routing-ext-03#section-2.2.2
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |              Type             |            Length             |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |     Flags     |     Weight    |            Reserved           |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |             OSPF Neighbor ID / IS-IS System-ID                |
# +                               +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    SID/Label/Index (variable)                 |
# +---------------------------------------------------------------+

#   Flags: 1 octet field of following flags:
#       0 1 2 3 4 5 6 7
#      +-+-+-+-+-+-+-+-+
#      |F|B|V|L|S|P|   |
#      +-+-+-+-+-+-+-+-+


@LinkState.register()
class LanAdjSegID(TLV):
    """
    Adjacency Segment id
    """
    TYPE = 1100
    TYPE_STR = 'lan_adj_sid'

    @classmethod
    def unpack(cls, data, pro_id):
        flags = ord(data[0:1])
        weight = ord(data[1:2])
        flag = {}
        if pro_id in [1, 2]:
            flag['F'] = flags >> 7
            flag['B'] = (flags << 1) % 256 >> 7
            flag['V'] = (flags << 2) % 256 >> 7
            flag['L'] = (flags << 3) % 256 >> 7
            flag['S'] = (flags << 4) % 256 >> 7
            flag['P'] = (flags << 5) % 256 >> 7
            tmp = binascii.b2a_hex(data[4:10]).decode("utf-8")
            chunks, chunk_size = len(tmp), int(len(tmp)/3)
            nei_or_sys_id = '.'.join([tmp[i:i+chunk_size] for i in range(0, chunks, chunk_size)])
            sid_index_label = int(binascii.b2a_hex(data[10:]), 16)
        else:  # 3, 6
            flag['B'] = flags >> 7
            flag['V'] = (flags << 1) % 256 >> 7
            flag['L'] = (flags << 2) % 256 >> 7
            flag['G'] = (flags << 3) % 256 >> 7
            flag['P'] = (flags << 4) % 256 >> 7
            nei_or_sys_id = str(netaddr.IPAddress(int(binascii.b2a_hex(data[4:8]), 16)))
            sid_index_label = int(binascii.b2a_hex(data[8:]), 16)
        return cls(value={
            "flags": flag,
            "weight": weight,
            "nei_or_sys_id": nei_or_sys_id,
            "value": sid_index_label
        })
