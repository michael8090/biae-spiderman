'''
Created on Sep 12, 2012

@author: hidn
'''

from crawler.repost import WeiboRepostAPI
from dao.repost import RepostDao
from dao.status import StatusDao
import util
from dao.user import UserDao
from crawler.comment import WeiboCommentAPI
from dao.comment import CommentDao


class CrawlRepostsAndCommentsForStatusTask:
    
    def __init__(self):
        pass
    
    def run(self):
        try:
            # Prepare DAOs.
            conn = util.get_crawler_connection()
            statusDao = StatusDao(conn)
            repostDao = RepostDao(conn)
            userDao = UserDao(conn)
            commentDao = CommentDao(conn)
    
            # Prepare APIs.
            client = util.get_weibo_client()
            repostAPI = WeiboRepostAPI(client)
            commentAPI = WeiboCommentAPI(client)

            # Fetch all statuses in DB.
            r_statuses = statusDao.getAllStatuses()


            # Fetch reposts, comments and authors of the statuses.  
            j_all_reposts = []
            j_all_comments =[]
            j_all_authors = []

            for r_status in r_statuses:
                status_id = r_status['id_status']

                j_reposts = repostAPI.get_reposts_of_status(status_id)
                j_repost_authors = (o['user'] for o in filter(self._has_user, j_reposts)) 

                j_comments = commentAPI.get_comments_on_status(status_id)
                j_comment_authors = (o['user'] for o in filter(self._has_user, j_comments)) 

                j_all_reposts.extend(j_reposts)
                j_all_comments.extend(j_comments)
                j_all_authors.extend(j_repost_authors)
                j_all_authors.extend(j_comment_authors)
    
            repostDao.insert_reposts(j_all_reposts)
            commentDao.insert_comments(j_all_comments)
            userDao.insert_users(j_all_authors)

        finally:    
            conn.close()
        
    @staticmethod
    def _has_user(j_comment_or_repost):
        user = j_comment_or_repost.get('user')
        if not user is None:
            return True

if __name__ == '__main__':
    CrawlRepostsAndCommentsForStatusTask().run()
