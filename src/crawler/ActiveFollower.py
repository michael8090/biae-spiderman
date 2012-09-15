'''ActiveFollower's methods
'''
import types
import MySQLdb

import util
from conf import *
from PublicToken import PublicToken
from WeiboClient import WeiboClient
from dao.user import UserDao

class ActiveFollower(WeiboClient):

    iRelationshipSQLTemplate = "INSERT INTO Followers (id_user, id_follower, is_ActiveFun) VALUES \
            (%s, %s, TRUE) ON DUPLICATE KEY UPDATE is_ActiveFun=TRUE;"
            
    mAPI = 'friendships/followers/active'
    
    def __init__(self, iUid):
        self.mUid = iUid
        self.activeUsers = []
        #only use the first row of public tokens right now, you can handle more if you want
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, jActiveUsers):
        assert(type(jActiveUsers) == types.ListType)
        
        try:
            conn = util.get_crawler_connection()
            dao = UserDao(conn)
            dao.insert_users(jActiveUsers)
            conn.close()
        except Exception, e:
            print 'Error when insert active user into Database because of: %s' % (e, )
                
        for activeUser in jActiveUsers:
            iRelationshipSQL = self.iRelationshipSQLTemplate % (self.mUid, activeUser['id'])
            
            try:
                conn = util.get_crawler_connection()
                cursor = conn.cursor()
                cursor.execute(iRelationshipSQL)
                cursor.close()
                conn.commit()
                conn.close()
            except Exception, e:
                print 'Error when insert active user relationship into Database because of: %s' % (e, )
    
    #fetch from Weibo and call sendToDB
    def process(self):
        iParams = {}
        iParams['uid'] = self.mUid
        #mPublicToken is a list:['uid', 'access_token']
        iParams['access_token'] = self.mPublicToken[1]
        iParams['count'] = 200
        lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
        if type(lJsonResult) == types.DictType and not lJsonResult.has_key('error'):
            self.activeUsers = lJsonResult['users']
            self._sendToDB(self.activeUsers)
            

    def getActiveUsers(self):
        return self.activeUsers