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
from dao.user import UserDao


class RepostCrawlTask:
    
    def __init__(self):
        pass
    
    def run(self):
        try:
            conn = util.get_crawler_connection()
            statusDao = StatusDao(conn)
            repostDao = RepostDao(conn)
            userDao = UserDao(conn)
    
            client = util.get_weibo_client()
            crawler = WeiboRepostAPI(client)

            statuses = statusDao.getAllStatuses()

            j_all_reposts = []
            j_all_authors = []

            for status in statuses:
                j_reposts = crawler.get_reposts_of_status(status['id'])
                
                j_authors = (repost['user'] for repost in j_reposts) 
                
                j_all_reposts.extend(j_reposts)
                j_all_authors.extend(j_authors)
    
            repostDao.insert_reposts(j_all_reposts)
            userDao.insert_users(j_all_authors)

        finally:    
            conn.close()

