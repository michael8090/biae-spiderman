'''WeiboUser's methods
'''

from PublicToken import PublicToken
from WeiboClient import WeiboClient

class WeiboUser(WeiboClient):
    
    API = 'users/show'
    
    def __init__(self,client):
        #only use the first row of public tokens right now, you can handle more if you want
        #WeiboClient.__init__(self, PublicToken.getPublicToken())
        self._client = client
    
    def getUser(self, userId):
        params = {
                  'uid': userId
                  #'access_token': self.mPublicToken[1]
                  }
        user = self._client.fetchUsingAPI(self.API, params)
        return user
