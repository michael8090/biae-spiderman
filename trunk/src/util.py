'''
Created on Sep 11, 2012

@author: yiliu
'''

import MySQLdb
from dateutil import parser
from calendar import timegm
from crawler.WeiboClient import WeiboClient
from crawler.PublicToken import PublicToken
import types


from crawler.conf import *


def parse_weibo_time_string(s):
    dt = parser.parse(s)
    return timegm(dt.utctimetuple())
    

def parse_long(s, default = None, base = 10):
    return long(s, base) if s != '' else default 

def get_crawler_connection():
    return MySQLdb.connect(host=gDBHost, port=gDBPort,
                                   user=gDBUser, passwd=gDBPassword,
                                   db=gDBSchema, charset="utf8")

def get_weibo_client():
    return WeiboClient(PublicToken.getPublicToken()[0])

def remove_InvalideChar_utf16(s):
    high_min = u'\ud800'
    high_max = u'\udbff'
    low_min = u'\udc00'
    low_max = u'\udfff'
    result = ''
    for i in range(0,len(s)):
        if not (s[i] >= high_min and s[i] <= high_max) or (s[i] >= low_min and s[i] <= low_max):
            result += s[i]
    return result
def remove_InvalideChar_utf8(s):
    result = ''
    ignoreNumber = 0
    for i in range(0,len(s)):
        if ignoreNumber != 0:
            ignoreNumber = ignoreNumber-1
            continue
        if s[i] < '\xf0':
            result += s[i]
        if s[i] >= '\xf0' and s[i] <'\xf8':
            ignoreNumber = 4
        if s[i] >= '\xf8' and s[i] < '\xfc':
            ignoreNumber = 5
        if s[i] >= 'x\fc' and s[i] <= '\xfd':
            ignoreNumver = 6
    return result
    
        
        
    

if __name__ == '__main__':
    print parse_weibo_time_string('Wed Sep 12 16:23:00 +0800 2012')
