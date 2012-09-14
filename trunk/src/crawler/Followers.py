'''Followers's methods
'''

import json
import MySQLdb
import types

import util
from crawler.conf import *
from dao.user import UserDao
from PublicToken import PublicToken
from WeiboClient import WeiboClient

def getNULL(s):
    if s=='':
        return 'NULL'
    else:
        return s

class Followers(WeiboClient):
    mSQLStatement = "INSERT INTO Followers \
                (id_user, id_follower, is_ActiveFun, INSERT_TIMESTAMP) \
                VALUES %s ON DUPLICATE KEY UPDATE id_user=id_user;"
    mSQLValueStatement = "(%s,%s,%s,current_timestamp),"
                
    mAPI = 'friendships/followers'
    
    def __init__(self, iUid):
        self.mUid = iUid
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, iJsonData):
        assert(type(iJsonData) == types.ListType)
        
        lValueStatement = ""
        for lInterator in iJsonData:
            lValueStatement += (self.mSQLValueStatement % 
                                (self.mUid,lInterator['id'],0))
            lInterator['description'] = util.remove_InvalideChar_utf16(lInterator['description'])
        lSQLStatement = self.mSQLStatement % (lValueStatement[:-1])
        print('SQL for  Followers ready.')
        
        try:
            conn = util.get_crawler_connection()
            dao = UserDao(conn)
            dao.insert_users(iJsonData)
            conn.close()
        except Exception, e:
            print 'Error when insert Followers into Database for EUid = %s because of: %s' % (self.mUid, e)
            
        try:
            conn = util.get_crawler_connection()
            cursor = conn.cursor()
            cursor.execute(lSQLStatement)
            cursor.close()
            conn.commit()
            conn.close()
            print('Insert  Followers relationships to db done.')
        except Exception, e:
            print 'Error when insert Followers into Database for EUid = %s because of: %s' % (self.mUid, e) 
    
    #fetch from Weibo and call sendToDB
    def process(self):
        iParams = {}
        iParams['uid'] = self.mUid
        iParams['count'] = 200
        #mPublicToken is a list:['uid', 'access_token']
        iParams['access_token'] = self.mPublicToken[1]
        lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
        print('Get Json data for Followers done.')
        if type(lJsonResult) == types.ListType and len(lJsonResult) > 0:
            self._sendToDB(lJsonResult)

