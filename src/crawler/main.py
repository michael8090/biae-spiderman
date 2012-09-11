#! -*- coding: utf-8 -*-

from WeiboUser import WeiboUser
from WeiboFollower import WeiboFollower
from Status import Status
from EUser import EUser
from Tag import Tag
from conf import *

if __name__ == '__main__':

    #get EUser Ids
    EUserIds = EUser.getEUserIds()
    print EUserIds

    #for each WeiboUser ID, crawl its Profile:
    for EUserId in EUserIds:
        try:
            weiboUser = WeiboUser(EUserId)
            weiboUser.process()
        except Exception, e:
            print ("Error: Cannot crawl data for EUser ID=%s because of: %s" % (EUserId, str(e)))

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

