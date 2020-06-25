#!/usr/bin/ python
# coding: utf-8
# -*- coding: utf-8 -*-


import ConfigParser
import time
import requests
import json

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
            print data
            url = 'http://numen.sankuai.com/aiops/api/alarm'
            headers = {
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6ZmFsc2UsInVzZXJuYW1lIjoiemhhbmd6aGFuZzAzIn0.-yYOvmXGakukPQ8ju0_EH07axYxoeMaSIKk-uccM_Qc'}
            r = requests.post(url, headers=headers, json=data)
            result = r.json()
            print result
            return True
        except Exception, e:
            print 'error'
            print str(e)
            return False

if __name__ == '__main__':

	cp = ConfigParser.ConfigParser()
	cp.read('bmp_info')
	for i in cp.sections():
	
		for j in cp.options(i):
			if cp.get(i,j)=='down':
				msg = u'[网络通告]BGP邻居异常\n'\
				      u'[异常详情]交换机{i}的bgp邻居{j}down,请尽快处理\n'\
				      u'[异常时间]{time}'\
				      .format(i=i,j=j,time=time.strftime(b'%Y-%m-%d %H:%M:%S', time.localtime()))
				falcon_alert('BGP'+i,'xm','PROBLEM',msg,'ruanfei,shuangpeng.wu,zhangzhang03,liyan53,ningjianghang,caizhenyu,luchangkun,wangnaimiao,tangguangming','')
