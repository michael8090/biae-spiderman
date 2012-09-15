'''
Created on Sep 12, 2012

@author: hidn
'''
import MySQLdb
import types

from util import parse_weibo_time_string, parse_long

class StatusDao:
    def __init__(self, conn):
        self._conn = conn;

    def getAllStatuses(self):
        conn = self._conn

        try:
            cursor = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
            cursor.execute(self.SQL_GET_ALL_STATUSES)

            rows = cursor.fetchall()
            
            cursor.close()
            conn.commit()
        except Exception, e:
            raise
        
        return rows
    
    def insert_statuses(self, j_statuses):
        assert(type(j_statuses) is types.ListType)

        rows = []
        for jStatus in j_statuses:
            rows.append(self._mapRow(jStatus))

        try:
            conn = self._conn
            cursor = conn.cursor()
            cursor.executemany(self.SQL_INSERT_STATUS, rows)
            cursor.close()
            conn.commit()
        except Exception, e:
            raise
            #print 'Error when insert WeiboFollower into Database for uid = %s because of: %s' % (self.mUid, e) 
        
    @staticmethod
    def _mapRow(o):
        return (o['id'], parse_weibo_time_string(o['created_at']), o['text'],
                o['source'], o['favorited'], o['truncated'],
                parse_long(o['in_reply_to_status_id']),
                parse_long(o['in_reply_to_user_id']),
                parse_long(o['in_reply_to_screen_name']),
                o['mid'], o['reposts_count'], o['comments_count'], o['user']['id'])
    
        
    SQL_INSERT_STATUS = '''
INSERT INTO Status
        (id_status, create_time, text, source, is_favorited, is_truncated,
        in_reply_to_status_id, in_reply_to_user_id, in_reply_to_screen_name,
        mid,reposts_count,comments_count, id_user, INSERT_TIMESTAMP)
VALUES (%s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp)
ON DUPLICATE KEY UPDATE
        is_favorited=Values(is_favorited), is_truncated=Values(is_truncated),
        reposts_count=Values(reposts_count), comments_count=Values(comments_count);
'''.strip()
    
    SQL_GET_ALL_STATUSES = '''
SELECT id_status FROM status ORDER BY id_status
'''.strip()
