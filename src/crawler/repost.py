'''Reposts crawl
'''

from dao.repost import RepostDao
import util

class WeiboRepostAPI:

    API = 'statuses/repost_timeline'
    PAGE_SIZE = 200
    
    def __init__(self, client):
        self._client = client
    
    def get_reposts_of_status(self, status_id):
        api_params = {
                     'id' : status_id,
                     #mPublicToken is a list:['uid', 'access_token']
                     #'access_token' : self._client.mPublicToken[1],
                     'count' : self.PAGE_SIZE
                     }

        j_reposts = self._client.fetchUsingAPI(self.API, api_params)
        return j_reposts
    
    def get_reposts(self, status_id, since_id):
        api_params = {
                     'id' : status_id,
                     #mPublicToken is a list:['uid', 'access_token']
                     #'access_token' : self._client.mPublicToken[1],
                     'count' : self.PAGE_SIZE,
                     'since_id' : since_id
                     }

        j_reposts = self._client.fetchUsingAPI(self.API, api_params)
        return j_reposts


if __name__ == '__main__':
    client = util.get_weibo_client()
    crawler = WeiboRepostAPI(client)
    j_reposts = crawler.get_reposts_of_status(11142488790L)
    
    try:
        conn = util.get_crawler_connection()
        dao = RepostDao(conn)
        dao.insert_reposts(j_reposts)
    finally:
        conn.close()
