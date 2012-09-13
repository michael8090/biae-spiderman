#! -*- coding: utf-8 -*-

from ActiveFollower import ActiveFollower
from conf import *
from EUser import EUser
from Followers import Followers
from FollowersFollowing import FollowersFollowingV
from Status import Status
from Tag import Tag
#from WeiboFollower import WeiboFollower
from WeiboUser import WeiboUser

if __name__ == '__main__':

    #get EUser Ids
    EUserIds = EUser.getEUserIds()
    
    for EUserId in EUserIds:
        #for each EUser ID, crawl its Profile:
        try:
            WeiboUser(EUserId).process()
        except Exception, e:
            print ("Error: Cannot crawl EUser profile for EUser ID=%s because of: %s" % (EUserId, str(e)))
        print('WeiboUser done.')
        
        #for each EUser ID, crawl its followers and their Profiles:
        try:
            Followers(EUserId).process()
        except Exception, e:
            print ("Error: Cannot crawl follower data for EUser ID=%s because of: %s" % (EUserId, str(e)))
        print('Followers done.')
        
        #for each EUser ID, crawl its Status and their comments and reposts:
        try:
            Status(EUserId).process()
        except Exception, e:
            print ("Error: Cannot crawl Status data for EUser ID=%s because of: %s" % (EUserId, str(e)))        
        print('Status done.')
        
        #for each WeiboUser ID, crawl its ActiveFollowers and their following list(Only V stored in DB):    
        try:
            activefollowers = ActiveFollower(EUserId)
            activefollowers.process()
            activelist = activefollowers.getActiveUsers()
            for auser in activelist:
                try:
                    FollowersFollowingV(auser['id'],1).process()
                except Exception, e:
                    print ("Error: Cannot crawl FollowingV list for activeUser ID=%s because of: %s" % (auser['id'], str(e)))
        except Exception, e:
            print ("Error: Cannot crawl ActiveFollower for EUser ID=%s because of: %s" % (EUserId, str(e)))
        print('ActiveFollower done.')

    try:
        Tag().process()
    except Exception, e:
        print ("Error: Tag because of: %s" % (str(e), ))
    print('Tag done.')
    
##    #for each WeiboUser ID, crawl its followers' IDs:
##    for lUserID in gUsersVec:
##        try:
##            lWeiboFollower = WeiboFollower(lUserID)
##            lWeiboFollower.process()
##        except Exception, e:
##            print ("Error: Cannot crawl data for Weibo User ID=%s because of: %s" % (lUserID, str(e)))
    
    #for each WeiboUser ID, crawl its Status:
#    for lUserID in gUsersVec:
#        Status(lUserID).process()

