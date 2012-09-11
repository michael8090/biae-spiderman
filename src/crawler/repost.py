'''Reposts crawl
'''
import types

from WeiboClient import WeiboClient
from PublicToken import PublicToken
from dao.repost import RepostDao
import util

class WeiboRepostAPI:

    API = 'statuses/repost_timeline'
    PAGE_SIZE = 200
    
    def __init__(self, client):
        self._client = client
    
    def fetch(self, status_id):
        api_params = {
                     'id' : status_id,
                     #mPublicToken is a list:['uid', 'access_token']
                     'access_token' : self._client.mPublicToken[1],
                     'count' : self.PAGE_SIZE
                     }

        j_reposts = self._client.fetchUsingAPI(self.API, api_params)
        return j_reposts


if __name__ == '__main__':
    client = WeiboClient(PublicToken.getPublicToken()[0])
    crawler = WeiboRepostAPI(client)
    j_reposts = crawler.fetch(11142488790L)
    
    try:
        conn = util.get_crawler_connection()
        dao = RepostDao(conn)
        dao.insert_reposts(j_reposts)
    finally:
        conn.close()
