#! -*- coding: utf-8 -*-

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

if __name__ == '__main__':

    EUserIds = EUser.getEUserIds()
    
    userCrawler = WeiboUser()
    followerCrawler = Followers()
    statusCrawler = Status()
    weiboClient = util.get_weibo_client()
    repostCrawler = WeiboRepostAPI(weiboClient)
    commentCrawler = WeiboCommentAPI(weiboClient)
    
    try:
        conn = util.get_crawler_connection()
    except Exception, e:
        print ("ERROR: Init conn fail: %s" % (str(e), ))
        
    userDao = UserDao(conn)
    userCounterDao = UserCounterDao(conn)
    followerDao = FollowerDao(conn)
    statusDao = StatusDao(conn)
    statusCounterDao = StatusCounterDao(conn)
    repostDao = RepostDao(conn)
    commentDao = CommentDao(conn)
    
    for EUserId in EUserIds:
        try:
            user = userCrawler.getUser(EUserId)
            userDao.insert_users([user])
            userCounterDao.insert_usercounters([user])
        except Exception, e:
            print ("ERROR: Insert EUser fail: %s" % (str(e), ))
        print ("Insert EUser %s done." % (EUserId, ))
        
        try:
            followers = followerCrawler.getFollowers(EUserId)
            userDao.insert_users(followers)
            followerDao.insert_followers(EUserId, followers, 0)
        except Exception, e:
            print ("ERROR: Insert follower fail: %s" % (str(e), ))
        print ("Insert EUser %s's followers done." % (EUserId, ))
#        
#        try:
#            statuses = statusCrawler.getStatuses(EUserId)
#            print ('Status Count : %d'%(len(statuses)))
#            statusDao.insert_statuses(statuses)
#            statusCounterDao.insert_statuscounters(statuses)
#        except Exception, e:
#            print ("ERROR: Insert status fail: %s" % (str(e), ))
#        print ("Insert EUser %s's statuses done." % (EUserId, ))
