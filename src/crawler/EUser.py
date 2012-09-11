'''Method to fetch EUser Ids from database
'''
import MySQLdb
from conf import *

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
            conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
            cursor = conn.cursor()
            cursor.execute(lSQLStatement) 
            result = cursor.fetchall()
            cursor.close()
            conn.commit()
            conn.close()
        except Exception, e:
            print 'Error when load public token from Database for team %s because of: %s' % (gTeamID, e) 
        return result;
