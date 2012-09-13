'''
Created on Sep 11, 2012

@author: yiliu
'''
from dateutil import parser
from calendar import timegm
from crawler.WeiboClient import WeiboClient
from crawler.PublicToken import PublicToken


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

def fix_invalid_character(s):
    high_min = u'\ud800'
    high_max = u'\udbff'
    low_min = u'\udc00'
    low_max = u'\udfff'
    for i in len(s):
        if (s[i] >= high_min and s[i] <= high_max) or (s[i] >= low_min and s[i] <= low_max):
            s[i] = ' '

if __name__ == '__main__':
    print parse_weibo_time_string('Wed Sep 12 16:23:00 +0800 2012')
