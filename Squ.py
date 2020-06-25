#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
import json
REDIS_HOST = '127.0.0.1'
REDSI_PORT = 6379

class SquirrelFunc(object):

    def __init__(self,category):
        self.sq_client = redis.Redis(host=REDIS_HOST, port=REDSI_PORT, db=0)
        self.category = category



    def get_key(self, k ,category):
        return self.category+'_'+k

    def set(self, k, v):
        sqkey = self.get_key(k, self.category)

        return self.sq_client.set(sqkey, v)

    def get(self, k):
        sqkey = self.get_key(k, self.category)

        return self.sq_client.get(sqkey)

    def delete(self, k):
        sqkey = self.get_key(k, self.category)

        return self.sq_client.delete(sqkey)

    def hset(self, k, field, v):
        sqkey = self.get_key(k, self.category)

        return self.sq_client.hset(sqkey, field, v)

    def hmget(self, k, fields):
        sqkey = self.get_key(k, self.category)

        return self.sq_client.hmget(sqkey, fields)

    def setnx(self, k, v):
        sqkey = self.get_key(k, self.category)

        res = self.sq_client.setnx(sqkey, v)
        return res

    def expire(self, k, t):
        sqkey = self.get_key(k, self.category)

        return self.sq_client.expire(sqkey, t)

    def ttl(self, k):
        sqkey = self.get_key(k, self.category)
        res = self.sq_client.ttl(sqkey)
        return res

    def hdel(self, k, field):
        sqkey = self.get_key(k, self.category)

        return self.sq_client.hdel(sqkey,field)

    def hgetall(self, k):
        sqkey = self.get_key(k, self.category)
        return self.sq_client.hgetall(sqkey)
    # https://km.sankuai.com/page/68201288

if __name__ == '__main__':

    redis = SquirrelFunc('bgp_monitor')
    redis_key = 'bmp'
    host = '10.55.1.9'
    redis_bgp = redis.hgetall(redis_key)



    bgp_info = { 'as_path_list': [4205504000,4205504001], 'next_hop': '10.55.49.2', 'nlri_list': '10.55.6.0/32'}
    host_peer = {'sw_ip':host,'peer_ip': '10.55.49.2'}
    bgp_info_string = json.dumps(bgp_info)

    redis.hset(redis_key,bgp_info_string,json.dumps(host_peer))

    #a = redis.hgetall(redis_key)
    #print(a)
    #b = redis.hdel(redis_key,bgp_info_string)
    #print(b)
    c = redis.hgetall(redis_key)
    print(c)




