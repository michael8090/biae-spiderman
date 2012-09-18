'''
Created on 2012-9-18

@author: Michael
'''
import types

class VFriendsDao:
    
    def __init__(self, conn):
        self._conn = conn;
        
    def insert_VFriends(self, userID, vFriends, isActive):
        assert(type(vFriends) is types.ListType)
        
        rows = []
        for friend in vFriends:
            if type(friend) is types.DictionaryType:
                rows.append((friend['id'], userID))
            
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
VALUES (%s, %s, 1, 0)
ON DUPLICATE KEY UPDATE is_ActiveFun=1;
'''.strip()
