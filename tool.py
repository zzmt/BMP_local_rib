#!/usr/bin/python3.7
# coding: utf-8
# -*- coding: utf-8 -*-

import time
import requests
import json
import  IPy

def falcon_alert(dci_index, method,status, content,receivers,xmGroup):

        data = [{
            'method': method,
            'ts': int(time.time()),
            'priority': 1,
            'status': status,
            'receivers': receivers,
            'object': dci_index,
            'metric': '抖动',
            'env': 'prod',
            'source': 'BMP',
            'name': 'dci_info',
            'content': content,
            "noAggr":True,
            'onlyContent':True,
            'isMinute':2,
            'xmGroup':xmGroup,
        }]
        try:
            print(data)
            url = 'http://numen.sankuai.com/aiops/api/alarm'
            headers = {
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6ZmFsc2UsInVzZXJuYW1lIjoiemhhbmd6aGFuZzAzIn0.-yYOvmXGakukPQ8ju0_EH07axYxoeMaSIKk-uccM_Qc'}
            r = requests.post(url, headers=headers, json=data)
            result = r.json()
            return True
        except Exception as e:

            return False


def local_ip_2_local_sysname_sw_id(ip):
    cmdb_url = "http://syscmdb.sankuai.com/api/v0.1/ci/s?q=_type:netdev,netdev_ip:{sysname_ip}".format(sysname_ip=ip)
    local_dev_string = requests.get(cmdb_url)
    local_dev_json = json.loads(local_dev_string.text)
    sysname = local_dev_json.get('result')[0].get('netdev_name','')
    sw_id = local_dev_json.get('result')[0].get('_id','')
    return sysname,sw_id

def local_sw_ip(nei_ip):
    tmp = [nei_ip]
    b = []
    a = IPy.IP(nei_ip).make_net('255.255.255.252')
    for i in a:
        b.append(i.strNormal(3))
    local_ip_list = list(set(b)-set(tmp))
    local_ip_list.sort()

    return local_ip_list[1]


def local_sysname_port(sw_ip, nei_ip):
	sysname,sw_id = local_ip_2_local_sysname_sw_id(sw_ip)
	local_ip = local_sw_ip(nei_ip)
	url = "http://syscmdb.sankuai.com/api/v0.1/cirelations/{id}/second_cis?count=1000".format(id=sw_id)
	string_url = requests.get(url)
	json_url = json.loads(string_url.text)
	for i in json_url.get('second_cis'):

		if local_ip == i.get('netdev_port_ipaddrs', ['none'])[0]:
			return sysname,i.get('netdev_port_name')

if __name__ == '__main__':

        bgp_msg = u'[网络通告]BGP邻居异常\n' \
                      u'[异常详情]交换机{i}的bgp邻居{j}down,请尽快处理\n' \
                      u'[异常时间]{time}' \
                .format(i='peer_host', j='peer_ip', time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        falcon_alert('BGP+ peer_host', 'xm', 'PROBLEM', bgp_msg, 'zhangzhang03', '')