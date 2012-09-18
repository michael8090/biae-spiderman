'''Followers's methods
'''

from PublicToken import PublicToken
from WeiboClient import WeiboClient

class Followers(WeiboClient):
    
    API = 'friendships/followers'
    active_API = 'friendships/followers/active'
    
    def __init__(self,client):
        #WeiboClient.__init__(self, PublicToken.getPublicToken())
        self._client = client
    
    def getFollowers(self, userId):
        params = {
                  'uid': userId,
                  'count': 200,
                  #'access_token': self.mPublicToken[1]
                  }
        followers = self._client.fetchUsingAPI(self.API, params)
        return followers
    
    def getActiveFollowers(self, userId):
        params = {
                  'uid': userId,
                  'count': 200,
                  #'access_token': self.mPublicToken[1]
                  }
        
        activeFollowers = self._client.fetchUsingAPI(self.active_API, params)
        return activeFollowers['users']
