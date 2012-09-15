'''Method to fetch EUser Ids from database
'''

import util

gEUserIds = []

class EUser():
    @staticmethod
    def getEUserIds():
        global gEUserIds
        if not gEUserIds:
            mEUserInstance = EUser()
            ttEUserIds = mEUserInstance._loadEUserIdsFromDB()
            #print ttEUserIds
            for tEUserId in ttEUserIds:
                gEUserIds.append(tEUserId[0])
        return gEUserIds;
    
    def _loadEUserIdsFromDB(self):
        lSQLStatement = "SELECT  idUser from EUser;"
        try:
            conn = util.get_crawler_connection()
            cursor = conn.cursor()
            cursor.execute(lSQLStatement) 
            result = cursor.fetchall()
            cursor.close()
            conn.commit()
            conn.close()
        except Exception, e:
            print ("ERROR: Load EUser fail: %s" % (str(e), ))
        return result;
