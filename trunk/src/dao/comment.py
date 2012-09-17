'''
Created on Sep 12, 2012

@author: hidn
'''
import types

from util import parse_weibo_time_string, parse_long



class CommentDao(object):
    '''
    classdocs
    '''


    def __init__(self, conn):
        '''
        Constructor
        '''
        self._conn = conn
        
    def get_max_comment_id(self, statusId):
        try:
            conn = self._conn
            cursor = conn.cursor()
            cursor.execute(self.SQL_GET_MAX_COMMENT_ID % statusId)
            result = cursor.fetchall()
            cursor.close()
            conn.commit()
        except Exception, e:
            raise
        if len(result) == 1:
            return result[0][0]
        return 0
        
    def insert_comments(self, j_comments):
        conn = self._conn
        assert(type(j_comments) == types.ListType)

        rows = []
        for jComment in j_comments:
            if not jComment.has_key('user'):
#                print '>< user N/A for status %d repost %d' % (status_id, jComment['id'])
                continue

            if not jComment.has_key('status'):
#                print '>< orgin N/A for status %d repost %d' % (status_id, jComment['id'])
                continue
            
            rows.append(self._mapRow(jComment))

        try:
            conn.begin()
            cursor = conn.cursor()
            cursor.executemany(self.SQL_INSERT_COMMENTS, rows)
            cursor.close()
            conn.commit()
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


    SQL_INSERT_COMMENTS = """
INSERT INTO status_comment (comment_id, commented_status_id, user_id, created_time, 
    `text`, source, mid, replied_to_comment_id, INSERT_TIMESTAMP)
VALUES (%s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s, NULL)
ON DUPLICATE KEY UPDATE comment_id = comment_id;
""".strip()

    SQL_GET_MAX_COMMENT_ID = '''
SELECT MAX(comment_id) FROM status_comment
WHERE commented_status_id = %s;
'''