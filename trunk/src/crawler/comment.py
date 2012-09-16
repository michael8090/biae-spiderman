'''Comment Crawl
'''
import types

import util
from dao.comment import CommentDao


class WeiboCommentAPI:

    API = 'comments/show'
    PAGE_SIZE = 200
    
    def __init__(self, client):
        self._client = client
    

    #fetch from Weibo and call sendToDB
    def get_comments_on_status(self, status_id):
        
        api_params = {
                     'id' : status_id,
                     #mPublicToken is a list:['uid', 'access_token']
                     #'access_token' : self._client.mPublicToken[1],
                     'count' : self.PAGE_SIZE
                     }

        j_result = self._client.fetchUsingAPI(self.API, api_params)
        return j_result
   



if __name__ == '__main__':
    
    try:
        conn = util.get_crawler_connection()
        commentDao = CommentDao(conn)
        
        client = util.get_weibo_client()
        crawler = WeiboCommentAPI(client)
        j_comments = crawler.get_comments_on_status(11142488790L)
        if type(j_comments) == types.ListType and len(j_comments) > 0:
            commentDao.insert_comments(j_comments)

    finally:
        conn.close()
