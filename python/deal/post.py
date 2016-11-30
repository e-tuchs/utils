# -*- coding: utf-8 -*-
import logging
import urllib2
data=''
url = 'http://127.0.0.1:80/api/test.json'
req = urllib2.Request(
    url=url,
    data=data,
    headers={'Content-Type': 'text/xml; charset=utf-8'})
response = urllib2.urlopen(req)
print type(response)
print response.read()
