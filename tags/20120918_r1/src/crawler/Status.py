'''Status's methods
'''

from PublicToken import PublicToken
from WeiboClient import WeiboClient

class Status(WeiboClient):
                
    API = 'statuses/user_timeline'
    
    def __init__(self):
        WeiboClient.__init__(self, PublicToken.getPublicToken())

    def getStatuses(self, userId):
        params = {
                  'uid': userId,
                  'count': 200
                  #'access_token': self.mPublicToken[1]
                  }
        statuses = self.fetchUsingAPI(self.API, params)
        return statuses