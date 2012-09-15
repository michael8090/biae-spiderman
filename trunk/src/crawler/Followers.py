'''Followers's methods
'''

from PublicToken import PublicToken
from WeiboClient import WeiboClient

class Followers(WeiboClient):
    
    API = 'friendships/followers'
    active_API = 'friendships/followers/active'
    
    def __init__(self):
        WeiboClient.__init__(self, PublicToken.getPublicToken()[0])
    
    def getFollowers(self, userId):
        params = {
                  'uid': userId,
                  'count': 200,
                  'access_token': self.mPublicToken[1]
                  }
        followers = self.fetchUsingAPI(self.API, params)
        return followers
    
    def getActiveFollowers(self, userId):
        params = {
                  'uid': userId,
                  'count': 200,
                  'access_token': self.mPublicToken[1]
                  }
        
        activeFollowers = self.fetchUsingAPI(self.API, params)
        return activeFollowers
