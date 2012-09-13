'''Status's methods
'''

import json
import MySQLdb
import types

import util
from conf import *
from comment import WeiboCommentAPI
from dao.comment import CommentDao
from dao.repost import RepostDao
from dao.status import StatusDao
from PublicToken import PublicToken
from repost import WeiboRepostAPI
from util import *
from WeiboClient import WeiboClient

def getNULL(s):
    if s=='':
        return 'NULL'
    else:
        return s

class Status(WeiboClient):
    mSQLStatement = "INSERT INTO Status_Counter \
                (id_status,reposts_count,comments_count,INSERT_TIMESTAMP) \
                values %s;"
    mSQLValue_Status_Counter = "(%s,%s,%s,current_timestamp),"
                
    mAPI = 'statuses/user_timeline'
    
    def __init__(self, iUid):
        self.mUid = iUid
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, iJsonData):
        assert(type(iJsonData) == types.ListType)
        
        lValueStatement2 = ""
        repost_crawler = WeiboRepostAPI(self)
        comment_crawler = WeiboCommentAPI(self)

        try:
            conn = util.get_crawler_connection()
            dao = StatusDao(conn)
            dao.insert_statuses(iJsonData)
            
            for lInterator in iJsonData:
                lValueStatement2 += (self.mSQLValue_Status_Counter %
                                     (lInterator['id'],lInterator['reposts_count'],lInterator['comments_count']))
                lSQLStatement = self.mSQLStatement % (lValueStatement2[:-1], )
                
                repost_result = repost_crawler.get_reposts_of_status(lInterator['id'])
                comment_result = comment_crawler.get_comments_on_status(lInterator['id'])
                repost_dao = RepostDao(conn)
                repost_dao.insert_reposts(repost_result)
                comment_dao = CommentDao(conn)
                comment_dao.insert_comments(comment_result)
                
            print('SQL for Status ready.')
            cursor = conn.cursor()
            cursor.execute(remove_InvalideChar_utf16(lSQLStatement)) 
            cursor.close()
            conn.commit()
            conn.close()
            print('store Status data to DB done.')
        except Exception, e:
            print 'Error when insert Status into Database for uid = %s because of: %s' % (self.mUid, e) 
    
    #fetch from Weibo and call sendToDB
    def process(self):
        iParams = {}
        iParams['uid'] = self.mUid
        #mPublicToken is a list:['uid', 'access_token']
        iParams['access_token'] = self.mPublicToken[1]
        lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
        print('Get Json data for status done.')
        if type(lJsonResult) == types.ListType and len(lJsonResult) > 0:
            self._sendToDB(lJsonResult)

