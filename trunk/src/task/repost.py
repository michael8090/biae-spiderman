'''
Created on Sep 12, 2012

@author: hidn
'''

from crawler.repost import WeiboRepostAPI
from dao.repost import RepostDao
from dao.status import StatusDao
from crawler import WeiboClient
from crawler.PublicToken import PublicToken
import util


class RepostCrawlTask:
    
    def __init__(self):
        pass
    
    def run(self):
        try:
            conn = util.get_crawler_connection()
            statusDao = StatusDao(conn)
            repostDao = RepostDao(conn)
    
            PublicToken.getPublicToken()
            client = WeiboClient(PublicToken.getPublicToken()[0])
            crawler = WeiboRepostAPI(client)

            statuses = statusDao.getAllStatuses()

            j_reposts = []
            for status in statuses:
                j_reposts.extend(crawler.fetch(status['id']))
    
            j_reposts = crawler.fetch(11142488790L)
            repostDao.insert_reposts(j_reposts)

        finally:    
            conn.close()
        
