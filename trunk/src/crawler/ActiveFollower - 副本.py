'''ActiveFollower's methods
'''
import types
import MySQLdb

from conf import *
from PublicToken import PublicToken
<<<<<<< .mine
from FollowersFollowing import FollowersFollowingV
=======
from WeiboClient import WeiboClient
from dao.user import UserDao
>>>>>>> .r49

class ActiveFollower(WeiboClient):
<<<<<<< .mine
    mSQLStatement = "INSERT INTO WeiboUser (idUser, screen_name, name, province, city, \
            location, description, url, profile_image, domain, gender, avatar_large, \
            verified, verified_reason, INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP) VALUES \
            (%s, '%s', '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', %s, '%s', %s, '%s', \
            current_timestamp, current_timestamp)ON DUPLICATE KEY UPDATE idUser=idUser;"
=======
>>>>>>> .r49

    iRelationshipSQLTemplate = "INSERT INTO Followers (id_user, id_follower, is_ActiveFun) VALUES \
            (%s, %s, TRUE) ON DUPLICATE KEY UPDATE is_ActiveFun=TRUE;"
            
    mAPI = 'friendships/followers/active'
    
    def __init__(self, iUid):
        self.mUid = iUid
        #only use the first row of public tokens right now, you can handle more if you want
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
<<<<<<< .mine
    def _sendToDB(self, j_reposts):
        assert(type(j_reposts) == types.DictType)
        for activeUser in j_reposts['users']:
            lSQLStatement = self.mSQLStatement % (activeUser['id'], activeUser['screen_name'], activeUser['name'], \
                    activeUser['province'], activeUser['city'], activeUser["location"], \
                    activeUser['description'], activeUser['url'], activeUser["profile_image_url"], activeUser["domain"], \
                    (activeUser["gender"].find('f') == -1), activeUser["avatar_large"], activeUser["verified"], \
                    activeUser['verified_reason'])
            try:
                FollowersFollowingV(activeUser['id'],1).process()
            except Exception, e:
                print ("Error: Cannot crawl data for Weibo User ID=%s because of: %s" % (activeUser['id'], str(e)))
            lupdateRelationshipSQL = self.updateRelationshipSQL % (self.mUid, activeUser['id'])
=======
    def _sendToDB(self, jActiveUsers):
        assert(type(jActiveUsers) == types.DictType)
        
        try:
            conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
            dao = UserDao(conn)
            dao.insert_users(jActiveUsers['users'])
            conn.close()
        except Exception, e:
            print 'Error when insert active user into Database because of: %s' % (e, )
                
        for activeUser in jActiveUsers['users']:
            iRelationshipSQL = self.iRelationshipSQLTemplate % (self.mUid, activeUser['id'])
            
>>>>>>> .r49
            try:
                conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
                cursor = conn.cursor()
                cursor.execute(iRelationshipSQL)
                cursor.close()
                conn.commit()
                conn.close()
            except Exception, e:
                print 'Error when insert active user relationship into Database because of: %s' % (e, )
    
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
