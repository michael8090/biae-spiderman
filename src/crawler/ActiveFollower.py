'''ActiveFollower's methods
'''
import MySQLdb
import types
from WeiboClient import WeiboClient
from conf import *
from PublicToken import PublicToken

class ActiveFollower(WeiboClient):
    mSQLStatement = "INSERT INTO WeiboUser (idUser, screen_name, name, province, city, \
            location, description, url, profile_image, domain, gender, avatar_large, \
            verified, verified_reason, INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP) VALUES \
            (%s, '%s', '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', %s, '%s', %s, '%s', \
            current_timestamp, current_timestamp);"

    updateRelationshipSQL = "INSERT INTO Followers (id_user, id_follower, is_ActiveFun) VALUES \
            (%s, %s, TRUE) ON DUPLICATE KEY UPDATE is_ActiveFun=TRUE;"
            
    mAPI = 'friendships/followers/active'
    
    def __init__(self, iUid):
        self.mUid = iUid
        #only use the first row of public tokens right now, you can handle more if you want
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, j_reposts):
        assert(type(j_reposts) == types.DictType)
        for activeUser in j_reposts['users']:
            lSQLStatement = self.mSQLStatement % (activeUser['id'], activeUser['screen_name'], activeUser['name'], \
                    activeUser['province'], activeUser['city'], activeUser["location"], \
                    activeUser['description'], activeUser['url'], activeUser["profile_image_url"], activeUser["domain"], \
                    (activeUser["gender"].find('f') == -1), activeUser["avatar_large"], activeUser["verified"], \
                    activeUser['verified_reason'])
            lupdateRelationshipSQL = self.updateRelationshipSQL % (self.mUid, activeUser['id'])
            try:
                conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
                cursor = conn.cursor()
                cursor.execute(lSQLStatement)
                cursor.close()
                conn.commit()
                conn.close()
            except Exception, e:
                print 'Error when insert active user into Database for uid = %s because of: %s' % (self.mUid, e)

            try:
                conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
                cursor = conn.cursor()
                cursor.execute(lupdateRelationshipSQL)
                cursor.close()
                conn.commit()
                conn.close()
            except Exception, e:
                print 'Error when insert active user relationship into Database for uid = %s because of: %s' % (self.mUid, e)
    
    #fetch from Weibo and call sendToDB
    def process(self):
        iParams = {}
        iParams['uid'] = self.mUid
        #mPublicToken is a list:['uid', 'access_token']
        iParams['access_token'] = self.mPublicToken[1]
        iParams['count'] = 200
        lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
        if type(lJsonResult) == types.DictType and not lJsonResult.has_key('error'):
            self._sendToDB(lJsonResult)
