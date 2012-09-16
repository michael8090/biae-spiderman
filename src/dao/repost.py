'''
Created on Sep 12, 2012

@author: hidn
'''

import types

from util import parse_weibo_time_string, parse_long

class RepostDao:
    
    def __init__(self, conn):
        self._conn = conn;
        
    def insert_reposts(self, j_reposts):
        assert(type(j_reposts) is types.ListType)

        status_id = j_reposts[0]['retweeted_status']['id']

        rows = []
        for jRepost in j_reposts:
            if not jRepost.has_key('user'):
                # print '>< user N/A for status %d repost %d' % (status_id, jRepost['id'])
                continue

            if not jRepost.has_key('retweeted_status'):
                # print '>< orgin N/A for status %d repost %d' % (status_id, jRepost['id'])
                continue
            
            rows.append(self._mapRow(jRepost))

        try:
            conn = self._conn
            cursor = conn.cursor()
            cursor.executemany(self.SQL_INSERT_REPOSTS, rows)
            cursor.close()
            conn.commit()
        except Exception, e:
            raise
            #print 'Error when insert WeiboFollower into Database for uid = %s because of: %s' % (self.mUid, e) 
        
    @staticmethod
    def _mapRow(o):
        assert o.has_key('retweeted_status')
        return (o['id'], o['retweeted_status']['id'], o['user']['id'],
                 parse_weibo_time_string(o['created_at']), 
                 o['text'], o['source'], o['favorited'], o['truncated'],
                 parse_long(o['in_reply_to_status_id'], 0),
                 o['in_reply_to_screen_name'],
                 parse_long(o['mid']), o['reposts_count'], o['comments_count']
                 )        
    
        
    SQL_INSERT_REPOSTS = '''
INSERT INTO repost (repost_id, retweeted_status_id, user_id, created_time, 
    text, source, favorited, truncated, in_reply_to_status_id,
    in_reply_to_screen_name, mid, reposts_count, comments_count, 
    INSERT_TIMESTAMP)
VALUES (%s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
ON DUPLICATE KEY UPDATE
    favorited = VALUES(favorited), truncated = VALUES(truncated),
    reposts_count = VALUES(reposts_count),
    comments_count = VALUES(comments_count);
'''.strip()
        