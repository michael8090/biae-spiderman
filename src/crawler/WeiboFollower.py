'''WeiboFollwer's methods
'''
import MySQLdb
import json
import types
from WeiboClient import WeiboClient
from conf import *
from PublicToken import PublicToken

class WeiboFollower(WeiboClient):
    mSQLStatement = "INSERT INTO Relationships (idFriend, idFollower, relationship_status, \
                INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP) VALUES %s ON DUPLICATE KEY UPDATE \
                relationship_status=Values(relationship_status);"
    mSQLValueStatement = "(%s, %s, %s, current_timestamp, current_timestamp),"
                
    mAPI = 'friendships/followers/ids'
    
    def __init__(self, iUid):
        self.mUid = iUid
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, j_reposts):
        assert(type(j_reposts) == types.ListType)
        lValueStatement = ""
        for lFollower in j_reposts:
            lValueStatement += (self.mSQLValueStatement % (self.mUid, lFollower, 1))
            lSQLStatement = self.mSQLStatement % lValueStatement[:len(lValueStatement) - 1]

        try:
            conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
            cursor = conn.cursor()
            cursor.execute(lSQLStatement) 
            cursor.close()
            conn.commit()
            conn.close()
        except Exception, e:
            print 'Error when insert WeiboFollower into Database for uid = %s because of: %s' % (self.mUid, e) 
    
    #fetch from Weibo and call sendToDB
    def process(self):
        iParams = {}
        iParams['uid'] = self.mUid
        #mPublicToken is a list:['uid', 'access_token']
        iParams['access_token'] = self.mPublicToken[1]
        #fetch 4000 followers IDs per page
        iParams['count'] = 4000
        lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
        if type(lJsonResult) == types.ListType and len(lJsonResult) > 0:
            self._sendToDB(lJsonResult)

