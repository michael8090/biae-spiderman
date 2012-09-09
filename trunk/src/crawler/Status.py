'''Status's methods
'''
import MySQLdb
import json
import types
from WeiboClient import WeiboClient
from conf import *
from PublicToken import PublicToken

class Status(WeiboClient):
    mSQLStatement = "INSERT INTO Status \
                (idStatus, mid, id_creatorUID, \
                id_crawlerUID, source,text,is_truncated,is_favorited,\
                created_time,in_reply_to_screen_name,in_reply_to_status_id,\
                in_reply_to_user_id,INSERT_TIMESTAMP,LAST_UPDATE_TIMESTAMP) \
                VALUES %s;"
    mSQLValueStatement = "(%s,%s,%s,%s,'%s','%s',%s,%s,'%s',%s,%s,current_timestamp,current_timestamp),"
                
    mAPI = 'statuses/user_timeline'
    
    def __init__(self, iUid):
        self.mUid = iUid
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, iJsonData):
        assert(type(iJsonData) == types.ListType)
        lValueStatement = ""
        for lInterator in iJsonData:
            lValueStatement += (self.mSQLValueStatement % (lInterator['id'],lInterator['mid'],\
                lInterator['user']['id'],lInterator['source'],lInterator['text'],\
                lInterator['truncated'],lInterator['favorited'],lInterator['created_at'],\
                lInterator['in_reply_to_screen_name'],lInterator['in_reply_to_status_id'],\
                lInterator['in_reply_to_user_id']))
            lSQLStatement = self.mSQLStatement % lValueStatement[:len(lValueStatement) - 1]
    

        print(lSQLStatement)
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
        lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
        print(lJsonResult)
        if type(lJsonResult) == types.ListType and len(lJsonResult) > 0:
            self._sendToDB(lJsonResult)

