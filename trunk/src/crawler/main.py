#! -*- coding: utf-8 -*-

from WeiboUser import WeiboUser
from WeiboFollower import WeiboFollower
from Status import Status
from conf import *

if __name__ == '__main__':
    for lUserID in gUsersVec:
        try:
            WeiboFollower(lUserID).process()
            WeiboUser(lUserID).process()
            Status(lUserID).process()

        except Exception, e:
            print ("Error: Cannot crawl data for Weibo User ID=%s because of: %s" % (lUserID, str(e)))
