'''Status's methods
'''

from PublicToken import PublicToken
from WeiboClient import WeiboClient

class Status(WeiboClient):
                
    API = 'statuses/user_timeline'
    
    def __init__(self, client):
        #WeiboClient.__init__(self, PublicToken.getPublicToken())
        self._client = client

    def getStatuses(self, userId):
        params = {
                  'uid': userId,
                  'count': 200
                  #'access_token': self.mPublicToken[1]
                  }
        statuses = self._client.fetchUsingAPI(self.API, params)
        return statuses
