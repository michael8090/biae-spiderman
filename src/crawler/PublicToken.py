'''Method to fetch public tokens from database
'''
import MySQLdb
from conf import *

gPublicTokens = None

class PublicToken():
    @staticmethod
    def getPublicToken():
        global gPublicTokens
        if not gPublicTokens:
            mPublicTokenInstance = PublicToken()
            gPublicTokens = mPublicTokenInstance._loadPublicTokenFromDB()        
        return gPublicTokens; 
    
    def _loadPublicTokenFromDB(self):
        lSQLStatement = "SELECT  UserID, Access_Token from Public_Token_Pool WHERE TokenStatus = 1;"
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


