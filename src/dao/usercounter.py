'''
Created on 2012-9-15

@author: shezepo
'''
import types

class UserCounterDao:
    
    def __init__(self, conn):
        self._conn = conn;
        
    def insert_usercounters(self, j_users):
        assert(type(j_users) is types.ListType)
        
        rows = []
        for jUser in j_users:
            rows.append(self._mapRow(jUser))
            
        try:
            conn = self._conn
            cursor = conn.cursor()
            cursor.executemany(self.SQL_INSERT_USERCOUNTERS, rows)
            cursor.close()
            conn.commit()
        except Exception, e:
            raise
    
    @staticmethod
    def _mapRow(o):
        return (o['id'], o['followers_count'], o['friends_count'], o['statuses_count'])
        
    SQL_INSERT_USERCOUNTERS = '''
INSERT INTO UserCounters (idUser, followers_count, friends_count,
        statuses_count, INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP)
VALUES (%s, %s, %s, %s, current_timestamp, current_timestamp) on duplicate key update idUser=idUser;
'''.strip()
