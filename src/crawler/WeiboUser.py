'''WeiboUser's methods
'''
import MySQLdb
import types
from WeiboClient import WeiboClient
from conf import *
from PublicToken import PublicToken

class WeiboUser(WeiboClient):
    mSQLStatement = "INSERT INTO WeiboUser (idUser, screen_name, name, province, city, \
            location, description, url, profile_image, domain, gender, avatar_large, \
            verified, verified_reason, INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP) VALUES \
            (%s, '%s', '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', %s, '%s', %s, '%s', \
            current_timestamp, current_timestamp);"

    mCounterSQLStatement = "INSERT INTO UserCounters (idUser, followers_count, friends_count, \
            statuses_count, INSERT_TIMESTAMP, LAST_UPDATE_TIMESTAMP) VALUES \
            (%s, %s, %s, %s, current_timestamp, current_timestamp);"
            
    mAPI = 'users/show'
    
    def __init__(self, iUid):
        self.mUid = iUid
        #only use the first row of public tokens right now, you can handle more if you want
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    #send json data to database
    def _sendToDB(self, iJsonData):
        assert(type(iJsonData) == types.DictType)
        lSQLStatement = self.mSQLStatement % (iJsonData['id'], iJsonData['screen_name'], iJsonData['name'], \
                    iJsonData['province'], iJsonData['city'], iJsonData["location"], \
                    iJsonData['description'], iJsonData['url'], iJsonData["profile_image_url"], iJsonData["domain"], \
                    (iJsonData["gender"].find('f') == -1), iJsonData["avatar_large"], iJsonData["verified"], \
                    iJsonData['verified_reason'])
        lCounterSQLStatement = self.mCounterSQLStatement % (iJsonData['id'], iJsonData['followers_count'], \
                                                            iJsonData['friends_count'], iJsonData['statuses_count'])
        try:
            conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
            cursor = conn.cursor()
            cursor.execute(lSQLStatement)
            cursor.close()
            conn.commit()
            conn.close()            
        except Exception, e:
            print 'Error when insert WeiboUser into Database for uid = %s because of: %s' % (self.mUid, e)

        try:
            conn = MySQLdb.connect(host=gDBHost, port=gDBPort, user=gDBUser, passwd=gDBPassword, db=gDBSchema, charset="utf8")
            cursor = conn.cursor()
            cursor.execute(lCounterSQLStatement)
            cursor.close()
            conn.commit()
            conn.close()            
        except Exception, e:
            print 'Error when insert UserCounters into Database for uid = %s because of: %s' % (self.mUid, e)
    
    #fetch from Weibo and call sendToDB
    def process(self):
        iParams = {}
        iParams['uid'] = self.mUid
        #mPublicToken is a list:['uid', 'access_token']
        iParams['access_token'] = self.mPublicToken[1]
        lJsonResult = self.fetchUsingAPI(self.mAPI, iParams)
        if type(lJsonResult) == types.DictType and not lJsonResult.has_key('error'):
            self._sendToDB(lJsonResult)
