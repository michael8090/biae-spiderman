'''
Created on 2012-9-15

@author: shezepo
'''
import types

class FollowerDao:
    
    def __init__(self, conn):
        self._conn = conn;
        
    def insert_followers(self, friendId, j_users, isActive):
        assert(type(j_users) is types.ListType)
        
        rows = []
        for jUser in j_users:
            rows.append((friendId, jUser['id']))
            
        try:
            conn = self._conn
            cursor = conn.cursor()
            if isActive == 0:
                cursor.executemany(self.SQL_INSERT_FOLLOWERS, rows)
            else:
                cursor.executemany(self.SQL_INSERT_ACTIVE_FOLLOWERS, rows)
            cursor.close()
            conn.commit()
        except Exception, e:
            raise
        
    SQL_INSERT_FOLLOWERS = '''
INSERT INTO Followers
        (id_user, id_follower, is_ActiveFun, INSERT_TIMESTAMP)
VALUES (%s, %s, 0, current_timestamp)
ON DUPLICATE KEY UPDATE
	INSERT_TIMESTAMP = IF(INSERT_TIMESTAMP = 0, VALUES(INSERT_TIMESTAMP), INSERT_TIMESTAMP);
'''.strip()

    SQL_INSERT_ACTIVE_FOLLOWERS = '''
INSERT INTO Followers
        (id_user, id_follower, is_ActiveFun, INSERT_TIMESTAMP)
VALUES (%s, %s, 1, current_timestamp)
ON DUPLICATE KEY UPDATE is_ActiveFun=1;
'''.strip()
