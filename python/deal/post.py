# -*- coding: utf-8 -*-
import urllib2

DEF_HEAD = {'Content-Type': 'application/json; charset=utf-8'}


def post_data(req_url, req_data, headers=DEF_HEAD):
    req = urllib2.Request(url=req_url, data=req_data, headers=headers)
    response = urllib2.urlopen(req)
    msg_resp = response.read()
    return msg_resp
