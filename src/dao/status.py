'''
Created on Sep 12, 2012

@author: hidn
'''
import MySQLdb



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
    
    SQL_GET_ALL_STATUSES = '''
SELECT id_status FROM status ORDER BY id_status
'''.strip()
