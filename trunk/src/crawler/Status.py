'''Status's methods
'''
import MySQLdb
import json
import types
from WeiboClient import WeiboClient
from conf import *
from PublicToken import PublicToken
from util import *

def getNULL(s):
    if s=='':
        return 'NULL'
    else:
        return s

class Status(WeiboClient):
    mSQLStatement = "INSERT INTO Status \
                (id_status, create_time, text, \
                source, is_favorited,is_truncated,\
                in_reply_to_status_id,in_reply_to_user_id,in_reply_to_screen_name,\
                mid,reposts_count,comments_count,\
                id_user,INSERT_TIMESTAMP) \
                VALUES %s ON DUPLICATE KEY UPDATE \
                is_favorited=Values(is_favorited), is_truncated=Values(is_truncated), \
                reposts_count=Values(reposts_count), comments_count=Values(comments_count);\
                INSERT INTO Status_Counter \
                (id_status,reposts_count,comments_count,INSERT_TIMESTAMP) \
                values %s;"
    mSQLValueStatement = "(%s,%s,'%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,current_timestamp),"
    mSQLValue_Status_Counter = "(%s,%s,%s,current_timestamp),"
                
    mAPI = 'statuses/user_timeline'
    
    def __init__(self, iUid):
        self.mUid = iUid
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, iJsonData):
        assert(type(iJsonData) == types.ListType)
        lValueStatement = ""
        lValueStatement2 = ""
        for lInterator in iJsonData:
            lValueStatement += (self.mSQLValueStatement % 
                                (lInterator['id'],parse_weibo_time_string(lInterator['created_at']),MySQLdb.escape_string(lInterator['text']),\
                                MySQLdb.escape_string(lInterator['source']),lInterator['favorited'],lInterator['truncated'],\
                                getNULL(lInterator['in_reply_to_status_id']),getNULL(lInterator['in_reply_to_user_id']),getNULL(lInterator['in_reply_to_screen_name']),\
                                lInterator['mid'],lInterator['reposts_count'],lInterator['comments_count'],\
                                lInterator['user']['id']))
            lValueStatement2 += (self.mSQLValue_Status_Counter %
                                 (lInterator['id'],lInterator['reposts_count'],lInterator['comments_count']))
            lSQLStatement = self.mSQLStatement % (lValueStatement[:len(lValueStatement) - 1],lValueStatement2[:-1])
    
        #lSQLStatement = MySQLdb.escape_string(lSQLStatement.encode('utf8','ignore'))
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

