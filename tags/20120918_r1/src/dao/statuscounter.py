'''
Created on 2012-9-15

@author: shezepo
'''
import types

class StatusCounterDao:
    
    def __init__(self, conn):
        self._conn = conn;
        
    def insert_statuscounters(self, j_statuses):
        assert(type(j_statuses) is types.ListType)
        
        rows = []
        for jStatus in j_statuses:
            if type(jStatus) == types.DictionaryType:
                rows.append(self._mapRow(jStatus))
            
        try:
            conn = self._conn
            cursor = conn.cursor()
            cursor.executemany(self.SQL_INSERT_STATUSCOUNTERS, rows)
            cursor.close()
            conn.commit()
        except Exception, e:
            raise
    
    @staticmethod
    def _mapRow(o):
        return (o['id'], o['reposts_count'], o['comments_count'])
        
    SQL_INSERT_STATUSCOUNTERS = '''
INSERT INTO Status_Counter
        (id_status,reposts_count,comments_count,INSERT_TIMESTAMP)
VALUES (%s,%s,%s,current_timestamp) on duplicate key update id_status=id_status;
'''.strip()
