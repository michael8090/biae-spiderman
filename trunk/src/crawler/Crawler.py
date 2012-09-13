#! -*- coding: utf-8 -*-

from WeiboUser import WeiboUser
#from WeiboFollower import WeiboFollower
#from Status import Status
from EUser import EUser
from Tag import Tag
from ActiveFollower import ActiveFollower
from conf import *
from Followers import Followers
from Status import Status

if __name__ == '__main__':

    #get EUser Ids
    EUserIds = EUser.getEUserIds()
    print EUserIds

    
    for EUserId in EUserIds:
        #for each WeiboUser ID, crawl its Profile:
        try:
            weiboUser = WeiboUser(EUserId)
            weiboUser.process()
        except Exception, e:
            print ("Error: Cannot crawl data for EUser ID=%s because of: %s" % (EUserId, str(e)))

        #for each WeiboUser ID, crawl its followers and their Profiles:
        try:
            Followers(EUserId).process()
        except Exception, e:
            print ("Error: Cannot crawl follower data for EUser ID=%s because of: %s" % (EUserId, str(e)))
     
        #for each WeiboUser ID, crawl its Status and their comments and reposts:
        try:
            Status(EUserId).process()
        except Exception, e:
            print ("Error: Cannot crawl Status data for EUser ID=%s because of: %s" % (EUserId, str(e)))        
            
#        try:
#            ActiveFollower(EUserId).process()
#        except Exception, e:
#            print ("Error: Cannot crawl ActiveFollower for EUser ID=%s because of: %s" % (EUserId, str(e)))

    try:
        Tag().process()
    except Exception, e:
        print ("Error: Tag because of: %s" % (str(e), ))
    
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

