import types

class UserDao:
    
    def __init__(self, conn):
        self._conn = conn;
        
    def insert_users(self, j_users):
        # TODO
        assert(type(j_users) == types.DictType)
        
        rows = []
        for jUser in j_users:
            rows.append(self._mapRow(jUser))
            
        try:
            conn = self._conn
            cursor = conn.cursor
            cursor.executemany(self.SQL_INSERT_REPOSTS, rows)
            cursor.close()
            conn.commit()
        except Exception, e:
            raise
    
    @staticmethod
    def _mapRow(o):
        return (o['id'], o['screen_name'], o['name'], o['provence'],
                 o['city'], o['location'], o['description'],
                 o['url'], o['profile_image_url'], o['domain'],
                 (o['gender'].find('f') == -1), o['avatar_large'],
                 o['verified'], o['verified_reason']
                 )
        
    SQL_INSERT_REPOSTS = '''
INSERT INTO WeiboUser (idUser, screen_name, name, province, city,
        location, description, url, profile_image, domain, gender, avatar_large,
        verified, verified_reason, INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP)
VALUES (%s, '%s', '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', %s, '%s', %s, '%s',
        current_timestamp, current_timestamp)
ON DUPLICATE KEY UPDATE LAST_UPDATE_TIMESTAMP=CURRENT_TIMESTAMP;
'''.strip()
