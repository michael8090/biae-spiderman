'''
Created on Sep 11, 2012

@author: yiliu
'''
import MySQLdb
from dateutil import parser

from crawler.conf import *


def parse_weibo_time_string(s):
    return parser.parse(s)

def parse_long(s, default = None, base = 10):
    return long(s, base) if s != '' else default 

def get_crawler_connection():
    return MySQLdb.connect(host=gDBHost, port=gDBPort,
                                   user=gDBUser, passwd=gDBPassword,
                                   db=gDBSchema, charset="utf8")
