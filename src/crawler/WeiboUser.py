'''WeiboUser's methods
'''

import MySQLdb
import types

import util
from conf import *
from dao.user import UserDao
from PublicToken import PublicToken
from WeiboClient import WeiboClient

class WeiboUser(WeiboClient):

    iUserCountersSQLTemplate = "INSERT INTO UserCounters (idUser, followers_count, friends_count, \
            statuses_count, INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP) VALUES \
            (%s, %s, %s, %s, current_timestamp, current_timestamp);"
            
    mAPI = 'users/show'
    
    def __init__(self, iUid):
        self.mUid = iUid
        #only use the first row of public tokens right now, you can handle more if you want
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, jUser):
        assert(type(jUser) == types.DictType)
        
        iUserCountersSQL = self.iUserCountersSQLTemplate % (jUser['id'], jUser['followers_count'], \
                                                            jUser['friends_count'], jUser['statuses_count'])
        try:
            conn = util.get_crawler_connection()
            dao = UserDao(conn)
            dao.insert_users([jUser])
            conn.close()
        except Exception, e:
            print 'Error when insert WeiboUser into Database for uid = %s because of: %s' % (self.mUid, e)

        try:
            conn = util.get_crawler_connection()
            cursor = conn.cursor()
            #cursor.execute(util.remove_InvalideChar_utf16(iUserCountersSQL))
            cursor.execute(iUserCountersSQL)
            cursor.close()
            conn.commit()
            conn.close()
        except Exception, e:
            print 'Error when insert UserCounters into Database for uid = %s because of: %s' % (self.mUid, e)
    
    #fetch from Weibo and call sendToDB
    def process(self):
        iParams = {}
        iParams['uid'] = self.mUid
        #mPublicToken is a list:['uid', 'access_token']
        iParams['access_token'] = self.mPublicToken[1]
        lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
        if type(lJsonResult) == types.DictType and not lJsonResult.has_key('error'):
            self._sendToDB(lJsonResult)
