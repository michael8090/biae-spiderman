'''VFriends's methods
'''

from PublicToken import PublicToken
from WeiboClient import WeiboClient

class VFriends(WeiboClient):
    
    API = 'friendships/friends'
    active_API = 'friendships/followers/active'
    
    def __init__(self,client):
        self._client = client
    
    def getVFriends(self, userId):
        params = {
                  'uid': userId,
                  'count': 200,
                  #'access_token': self.mPublicToken[1]
                  }
        friends = self._client.fetchUsingAPI(self.API, params)
        vfriends = []
        for friend in friends:
            if friend['verified']:
                vfriends.append(friend)
        return vfriends
