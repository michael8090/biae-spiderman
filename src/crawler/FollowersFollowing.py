'''FollowersFollowingV's methods
'''
import MySQLdb
import json
import types
from WeiboClient import WeiboClient
from conf import *
from PublicToken import PublicToken

def getNULL(s):
    if s=='':
        return 'NULL'
    else:
        return s

class FollowersFollowingV(WeiboClient):
    mSQLStatement = "INSERT INTO Followers \
                (id_user, id_follower, is_ActiveFun,INSERT_TIMESTAMP) \
                VALUES %s ON DUPLICATE KEY UPDATE id_user=id_user;"
    mSQLValueStatement = "(%s,%s,%s,current_timestamp),"
                
    mAPI = 'friendships/friends'
    isActive = 0
    
# for followers's profile
    mSQLStatement_fp = "INSERT INTO WeiboUser (idUser, screen_name, name, province, city, \
            location, description, url, profile_image, domain, gender, avatar_large, \
            verified, verified_reason, INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP) VALUES %s ON DUPLICATE KEY UPDATE LAST_UPDATE_TIMESTAMP=current_timestamp;"

    mSQLValueStatement_fp = "(%s, '%s', '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', %s, '%s', %s, '%s', \
            current_timestamp, current_timestamp),"

    
    def __init__(self, iUid,isActive):
        self.mUid = iUid
        self.isActive = isActive
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, iJsonData):
        assert(type(iJsonData) == types.ListType)
        lValueStatement = ""
        lValueStatement_fp = ""
        for lInterator in iJsonData:
            if(lInterator["verified"]):
                lValueStatement += (self.mSQLValueStatement % 
                                    (lInterator['id'],self.mUid,self.isActive))
                lValueStatement_fp += (self.mSQLValueStatement_fp % (lInterator['id'], MySQLdb.escape_string(lInterator['screen_name']), MySQLdb.escape_string(lInterator['name']), \
                            lInterator['province'], lInterator['city'], MySQLdb.escape_string(lInterator["location"]), \
                            MySQLdb.escape_string(lInterator['description']), MySQLdb.escape_string(lInterator['url']), MySQLdb.escape_string(lInterator["profile_image_url"]), MySQLdb.escape_string(lInterator["domain"]), \
                            (lInterator["gender"].find('f') == -1), MySQLdb.escape_string(lInterator["avatar_large"]), lInterator["verified"], \
                            MySQLdb.escape_string(lInterator['verified_reason'])))
                lSQLStatement = self.mSQLStatement % (lValueStatement[:-1])
                lSQLStatement_fp = self.mSQLStatement_fp % (lValueStatement_fp[:-1])
    
        #lSQLStatement = MySQLdb.escape_string(lSQLStatement.encode('utf8','ignore'))
        #print(lSQLStatement)
        print('SQL for FollowersFollowing ready.')
        try:
            conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
            cursor = conn.cursor()
            cursor.execute(lSQLStatement)
            cursor.execute(lSQLStatement_fp)
            cursor.close()
            conn.commit()
            conn.close()
            print('Store data for FollowersFollowing to DB done.')
        except Exception, e:
            print 'Error when insert WeiboFollower into Database for uid = %s because of: %s' % (self.mUid, e) 
    
    #fetch from Weibo and call sendToDB
    def process(self):
        iParams = {}
        iParams['uid'] = self.mUid
        #mPublicToken is a list:['uid', 'access_token']
        iParams['access_token'] = self.mPublicToken[1]
        lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
        #print(lJsonResult)
        print('Get Json data for FollowersFollowing done.')
        if type(lJsonResult) == types.ListType and len(lJsonResult) > 0:
            self._sendToDB(lJsonResult)

