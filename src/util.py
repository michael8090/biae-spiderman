'''
Created on Sep 11, 2012

@author: yiliu
'''
import MySQLdb
from crawler.conf import *


def parse_weibo_time_string(s):
    #TODO
    return 0

def parse_long(s, default = None, base = 10):
    return long(s, base) if s != '' else default 

def get_crawler_connection():
    return MySQLdb.connect(host=gDBHost, port=gDBPort,
                                   user=gDBUser, passwd=gDBPassword,
                                   db=gDBSchema, charset="utf8")
