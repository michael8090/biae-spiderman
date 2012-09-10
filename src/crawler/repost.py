'''WeiboFollwer's methods
'''
import MySQLdb
import json
import types
from WeiboClient import WeiboClient
from conf import *
from PublicToken import PublicToken
from time import sleep

def parse_weibo_time_string(s):
    #TODO
    return 0

def parse_long(s, default = None, base = 10):
    return long(s, base) if s != '' else default 

class WeiboRepost:
    SQL_TEMPLATE = """
INSERT INTO Repost (repost_id, retweeted_status_id, user_id, created_time, 
    text, source, favorited, truncated, in_reply_to_status_id,
    in_reply_to_screen_name, mid, reposts_count, comments_count, 
    INSERT_TIMESTAMP)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
ON DUPLICATE KEY UPDATE
    favorited = VALUES(favorited), truncated = VALUES(truncated),
    reposts_count = VALUES(reposts_count),
    comments_count = VALUES(comments_count);
""".strip()

    API = 'statuses/repost_timeline'
    PAGE_SIZE = 20
    
    def __init__(self, statusId):
        self._statusId = statusId
        self.wclient = WeiboClient(PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, iJsonData):
        
        assert(type(iJsonData) == types.ListType)

        retweeted_status_id = iJsonData[0]['retweeted_status']['id']

        rows = (
                (o['id'], retweeted_status_id, o['user']['id'],
                 parse_weibo_time_string(o['created_at']), 
                 o['text'], o['source'], o['favorited'], o['truncated'],
                 parse_long(o['in_reply_to_status_id'], 0),
                 o['in_reply_to_screen_name'],
                 parse_long(o['mid']), o['reposts_count'], o['comments_count']
                 )
                for o in iJsonData
                )

        try:
            conn = MySQLdb.connect(host=gDBHost, port=gDBPort,
                                   user=gDBUser, passwd=gDBPassword,
                                   db=gDBSchema, charset="utf8")
            cursor = conn.cursor()
            cursor.executemany(self.SQL_TEMPLATE, rows)
            cursor.close()
            conn.commit()
            conn.close()
        except Exception, e:
            raise
            #print 'Error when insert WeiboFollower into Database for uid = %s because of: %s' % (self.mUid, e) 
    
    #fetch from Weibo and call sendToDB
    def process(self):
        
        apiParams = {
                     'id' : self._statusId,
                     #mPublicToken is a list:['uid', 'access_token']
                     'access_token' : self.wclient.mPublicToken[1],
                     'count' : self.PAGE_SIZE
                     }

        jsonResult = self.wclient.fetchUsingAPI(self.API, apiParams)
        print `jsonResult`
        if type(jsonResult) == types.ListType and len(jsonResult) > 0:
            self._sendToDB(jsonResult)


if __name__ == '__main__':
    crawler = WeiboRepost(11142488790L)
    crawler.process()

