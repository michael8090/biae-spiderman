'''Tag's methods
'''
import MySQLdb
import types
import math
from WeiboClient import WeiboClient
from PublicToken import PublicToken
from conf import *

class Tag(WeiboClient):
    mSQLStatement = "INSERT INTO Tags (idUser, tagId, tag, weight, \
            INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP) VALUES %s"
    mSQLValueStatement = "(%s, %s, '%s', %s, current_timestamp, current_timestamp),"
                
    mAPI = 'tags/tags_batch'
    
    def __init__(self):
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, j_reposts):
        assert(type(j_reposts) == types.ListType)
        lValueStatement = ""
        for lUser in j_reposts:
            for lTag in lUser['tags']:
                for k, v in lTag.items():
                    if k != "weight":
                        lValueStatement += (self.mSQLValueStatement % (lUser['id'], k, v, lTag['weight']))
        lSQLStatement = self.mSQLStatement % lValueStatement[:len(lValueStatement) - 1]

        try:
            conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
            cursor = conn.cursor()
            cursor.execute(lSQLStatement) 
            cursor.close()
            conn.commit()
            conn.close()
        except Exception, e:
            print 'Error when insert Tag into Database because of: %s' % (e, )

    #fetch VUserId from database
    def _fetchFromDB(self):
        mSQLFetchVUserId = "SELECT idUser from WeiboUser where verified = TRUE;"
        try:
            conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
            cursor = conn.cursor()
            cursor.execute(mSQLFetchVUserId) 
            result = cursor.fetchall()
            cursor.close()
            conn.commit()
            conn.close()
        except Exception, e:
            print 'Error when load VUser ids from Database because of: %s' % (e, )
        VUserIds = []
        for VUserId in result:
            VUserIds.append(str(VUserId[0]))
        return VUserIds;
    
    #fetch from Weibo and call sendToDB
    def process(self):
        lUids = self._fetchFromDB()
        for i in range( int(math.ceil(len(lUids)/20.0)) ):
            mUids = ",".join(lUids[i*20:(i+1)*20])
            iParams = {}
            iParams['uids'] = mUids
            #mPublicToken is a list:['uid', 'access_token']
            iParams['access_token'] = self.mPublicToken[1]
            lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
            if type(lJsonResult) == types.ListType and len(lJsonResult) > 0:
                self._sendToDB(lJsonResult)
