'''Comment Crawl
'''
import types

from WeiboClient import WeiboClient
from PublicToken import PublicToken
import util
from util import parse_weibo_time_string, parse_long


class WeiboComment:
    SQL_TEMPLATE = """
INSERT INTO status_comment (comment_id, commented_status_id, user_id, created_time, 
    `text`, source, mid, replied_to_comment_id, INSERT_TIMESTAMP)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL)
ON DUPLICATE KEY UPDATE comment_id = comment_id;
""".strip()

    API = 'comments/show'
    PAGE_SIZE = 200
    
    def __init__(self, status_id):
        self._status_id = status_id
        self._wclient = WeiboClient(PublicToken.getPublicToken()[0])
    

    #fetch from Weibo and call sendToDB
    def process(self):
        
        api_params = {
                     'id' : self._status_id,
                     #mPublicToken is a list:['uid', 'access_token']
                     'access_token' : self._wclient.mPublicToken[1],
                     'count' : self.PAGE_SIZE
                     }

        j_result = self._wclient.fetchUsingAPI(self.API, api_params)
        if type(j_result) == types.ListType and len(j_result) > 0:
            self._sendToDB(j_result)
   
    #send json data to database
    def _sendToDB(self, j_comments):
        assert(type(j_comments) == types.ListType)

        status_id = j_comments[0]['status']['id']

        rows = []
        for jComment in j_comments:
            if not jComment.has_key('user'):
                print '>< user N/A for status %d repost %d' % (status_id, jComment['id'])
                continue

            if not jComment.has_key('status'):
                print '>< orgin N/A for status %d repost %d' % (status_id, jComment['id'])
                continue
            
            rows.append(self._mapRow(jComment))

        try:
            conn = util.get_crawler_connection()
            cursor = conn.cursor()
            cursor.executemany(self.SQL_TEMPLATE, rows)
            cursor.close()
            conn.commit()
            conn.close()
        except Exception, e:
            raise
            #print 'Error when insert WeiboFollower into Database for uid = %s because of: %s' % (self.mUid, e) 
    

    @staticmethod
    def _mapRow(o):
        
        reply_comment = o.get('reply_comment')
        reply_comment_id = reply_comment['id'] if not reply_comment is None else 0
        
        return (o['id'], o['status']['id'], o['user']['id'],
                 parse_weibo_time_string(o['created_at']), 
                 o['text'], o['source'], 
                 parse_long(o['mid']), reply_comment_id
                 )        


if __name__ == '__main__':
    crawler = WeiboComment(11142488790L)
    crawler.process()

