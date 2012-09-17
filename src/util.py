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
import sys
import traceback

from crawler.conf import *


def print_full_exception():
#    if output_file is None:
    output_file = sys.stderr
    type, error, tb = sys.exc_info()
    print type
    print error
    l = traceback.extract_stack()[:-2] + traceback.extract_tb(tb)
    traceback._print(output_file, 'Traceback (most recent call last):')
    traceback.print_list(l)

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
    tokens = PublicToken.getPublicToken()
    #print(tokens)
    return WeiboClient(tokens)

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
        is_invalide = True
        if ignoreNumber != 0:
            ignoreNumber = ignoreNumber-1
            continue
        if s[i] < '\xf0':
            result += s[i]
        if s[i] >= '\xf0' and s[i] <'\xf8':
            for j in range(1,4):
                if not (i+j < len(s) and (s[i+j] >= '\x80' and s[i+j] < '\xc0')):
                    is_invalide = False
                    break 
            if is_invalide:
                #print('invalid 4 bytes character found')
                ignoreNumber = 3
#                continue
#            else:
#                result += s[i]
        elif s[i] >= '\xf8' and s[i] < '\xfc':
            for j in range(1,5):
                if not (i+j < len(s) and (s[i+j] >= '\x80' and s[i+j] < '\xc0')):
                    is_invalide = False 
                    break
            if is_invalide:
                #print('invalid 5 bytes character found')
                ignoreNumber = 4
#                continue
#            else:
#                result += s[i]
        elif s[i] >= 'x\fc' and s[i] <= '\xfd':
            for j in range(1,6):
                if not (i+j < len(s) and (s[i+j] >= '\x80' and s[i+j] < '\xc0')):
                    is_invalide = False 
                    break
            if is_invalide:
                #print('invalid 6 bytes character found')
                ignoreNumber = 5
#                continue
#            else:
#                result += s[i]
    return result
    
        
        
    

if __name__ == '__main__':
    print parse_weibo_time_string('Wed Sep 12 16:23:00 +0800 2012')
