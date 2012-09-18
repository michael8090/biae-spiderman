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
from Tag import Tag
from WeiboUser import WeiboUser
from VFriends import VFriends
from dao.VFriendsDao import VFriendsDao

if __name__ == '__main__':

    EUserIds = EUser.getEUserIds()
    

    weiboClient = util.get_weibo_client()
    repostCrawler = WeiboRepostAPI(weiboClient)
    commentCrawler = WeiboCommentAPI(weiboClient)
    userCrawler = WeiboUser(weiboClient)
    followerCrawler = Followers(weiboClient)
    vFriendsCrawler = VFriends(weiboClient)
    
    try:
        conn = util.get_crawler_connection()
    except Exception, e:
        print ("ERROR: Init conn fail: %s" % (str(e), ))
        
    userDao = UserDao(conn)
    userCounterDao = UserCounterDao(conn)
    followerDao = FollowerDao(conn)
    repostDao = RepostDao(conn)
    commentDao = CommentDao(conn)
    vFriendsDao = VFriendsDao(conn)
    
    index = 0
    total = len(EUserIds)
    for EUserId in EUserIds:
        index = index + 1
        try:
            activeFollowers = followerCrawler.getActiveFollowers(EUserId)
            userDao.insert_users(activeFollowers)
            followerDao.insert_followers(EUserId, activeFollowers, 1)
        except Exception, e:
            print ("ERROR: Insert active follower fail: %s" % (str(e), ))
        print ("%d/%d Insert EUser %s's active followers done." % (index,total,EUserId))
        
        try:
            j = 0
            fc = len(activeFollowers)
            for aUser in activeFollowers:
                j = j + 1
                try:
                    #VFriends(aUser['id'],1).process()
                    vfriends = vFriendsCrawler.getVFriends(aUser['id'])
                    vFriendsDao.insert_VFriends(aUser['id'], vfriends, 1)
                    userDao.insert_users(vfriends)
                except Exception, e:
                    print ("ERROR: Insert VFriends fail: %s"% (str(e),))
                print ("%d/%d - %d/%d Insert Active Follower %s's VFriends done."%(index,total,j,fc,aUser['id']))
        except Exception, e:
            print ("ERROR: Insert VFriends fail: %s"% (str(e),))
            continue
        print ("%d/%d Insert Active Follower %s's VFriends done."%(index,total,aUser['id']))
    
    print('--------All EUsers done--------')
                
        

    try:
        Tag().process()
    except Exception, e:
        print ("Error: Tag because of: %s" % (str(e), ))
    print('Tag done.')
