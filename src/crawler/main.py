from Multi_Thread_Repost_Comment import *
import util

import util
from comment import WeiboCommentAPI
from dao.user import UserDao
from dao.usercounter import UserCounterDao
from dao.follower import FollowerDao
from dao.status import StatusDao
from dao.statuscounter import StatusCounterDao
from dao.repost import RepostDao
from dao.comment import CommentDao
from EUser import EUser
from Followers import Followers
from repost import WeiboRepostAPI
from Status import Status
from Tag import Tag
from WeiboUser import WeiboUser
from VFriends import VFriends

#from dao.repost import RepostDao
#from dao.comment import CommentDao
#from PublicToken import PublicToken
#from WeiboClient import WeiboClient
#import threading

#if __name__ == '__main__':
#    params = getParams()
#    threadCount = len(params['repostCrawlers'])
#    threads = []
#    for i in range(0,threadCount):
#        athread = threading.Thread(target = crawl_repost_and_comment, args = (i,params))
#        threads.append(athread)
#    for athread in threads:
#        athread.start()
#    
#    isRunning = True
#    while isRunning: 
#        isRunning = False
#        for athread in threads:
#            if athread.isAlive():
#                isRunning = True

if __name__ == '__main__':
    
    weiboClient = util.get_weibo_client()
    repostCrawler = WeiboRepostAPI(weiboClient)
    commentCrawler = WeiboCommentAPI(weiboClient)
#    userCrawler = WeiboUser(weiboClient)
#    followerCrawler = Followers(weiboClient)
#    statusCrawler = Status(weiboClient)
    
    try:
        conn = util.get_crawler_connection()
    except Exception, e:
        print ("ERROR: Init conn fail: %s" % (str(e), ))
        
#    userDao = UserDao(conn)
#    userCounterDao = UserCounterDao(conn)
#    followerDao = FollowerDao(conn)
#    statusDao = StatusDao(conn)
#    statusCounterDao = StatusCounterDao(conn)
    repostDao = RepostDao(conn)
    commentDao = CommentDao(conn)    

    try:
        cursor = conn.cursor()
        cursor.execute('select id_status from Status') 
        statuses = cursor.fetchall()
        cursor.close()
    except Exception, e:
        print ('Error when load Status from DB')
    print('Load Status from DB done.')
    

    
    for status in statuses:
        try:
            reposts = repostCrawler.get_reposts_of_status(status[0])
            repostDao.insert_reposts(reposts)
            print '.',
        except Exception, e:
            print ("ERROR: Insert reposts fail: %s" % (str(e), ))
            util.print_full_exception()
        try:
            comments = commentCrawler.get_comments_on_status(status[0])
            commentDao.insert_comments(comments)
            print '.',
        except Exception, e:
            print ("ERROR: Insert comments fail: %s" % (str(e), ))
            util.print_full_exception()
    print('All done.')
        
    
    