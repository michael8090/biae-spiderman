import types

class UserDao:
    
    def __init__(self, conn):
        self._conn = conn;
        
    def insert_users(self, j_users):
        # TODO
        assert(type(j_users) is types.ListType)
        
        rows = []
        for jUser in j_users:
            rows.append(self._mapRow(jUser))
            
        try:
            conn = self._conn
            cursor = conn.cursor()
            cursor.executemany(self.SQL_INSERT_REPOSTS, rows)
            cursor.close()
            conn.commit()
        except Exception, e:
            raise
    
    @staticmethod
    def _mapRow(o):
        if o['gender'].find('m') != -1:
            o['gender'] = 1
        else:
            if o['gender'].find('f') != -1:
                o['gender'] = 2
            else:
                o['gender'] = 3
            
        return (o['id'], o['screen_name'], o['name'], o['province'],
                 o['city'], o['location'], o['description'],
                 o['url'], o['profile_image_url'], o['domain'],
                 o['gender'], o['avatar_large'],
                 o['verified'], o['verified_reason']
                 )
        
    SQL_INSERT_REPOSTS = '''
INSERT INTO WeiboUser (idUser, screen_name, name, province, city,
        location, description, url, profile_image, domain, gender, avatar_large,
        verified, verified_reason, INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        current_timestamp, current_timestamp)
ON DUPLICATE KEY UPDATE LAST_UPDATE_TIMESTAMP=current_timestamp;
'''.strip()
