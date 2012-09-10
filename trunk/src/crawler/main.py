#! -*- coding: utf-8 -*-

from WeiboUser import WeiboUser
from WeiboFollower import WeiboFollower
from Status import Status
from conf import *

if __name__ == '__main__':
    #for each WeiboUser ID, crawl its Profile:
##    for lUserID in gUsersVec:
##        try:
##            lWeiboUser = WeiboUser(lUserID)
##            lWeiboUser.process()
##        except Exception, e:
##            print ("Error: Cannot crawl data for Weibo User ID=%s because of: %s" % (lUserID, str(e)))
##    
##    #for each WeiboUser ID, crawl its followers' IDs:
##    for lUserID in gUsersVec:
##        try:
##            lWeiboFollower = WeiboFollower(lUserID)
##            lWeiboFollower.process()
##        except Exception, e:
##            print ("Error: Cannot crawl data for Weibo User ID=%s because of: %s" % (lUserID, str(e)))
    
    #for each WeiboUser ID, crawl its Status:
    for lUserID in gUsersVec:
        try:
            Status(lUserID).process()
        except Exception, e:
            print ("Error: Cannot crawl data for Weibo User ID=%s because of: %s" % (lUserID, str(e)))