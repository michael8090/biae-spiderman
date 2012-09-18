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
            activeFollowers = followerCrawler.getActiveFollowers(EUserId)
            userDao.insert_users(activeFollowers)
            followerDao.insert_followers(EUserId, activeFollowers, 1)
        except Exception, e:
            print ("ERROR: Insert active follower fail: %s" % (str(e), ))
        print ("Insert EUser %s's active followers done." % (EUserId, ))
        
        try:
            for aUser in activeFollowers:
#                try:
#                    VFriends(aUser['id'],1).process()
#                except Exception, e:
#                    print ("ERROR: Insert VFriends fail: %s"% (str(e),))
#                print ("Insert Active Follower %s's VFriends done."%(aUser['id']))
                VFriends(aUser['id'],1).process()
                print ("Insert Active Follower %s's VFriends done."%(aUser['id']))
        except Exception, e:
            print ("ERROR: Insert VFriends fail: %s"% (str(e),))
            continue
        print ("Insert Active Follower %s's VFriends done."%(aUser['id']))
                
        

    try:
        Tag().process()
    except Exception, e:
        print ("Error: Tag because of: %s" % (str(e), ))
    print('Tag done.')
