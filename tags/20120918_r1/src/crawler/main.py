from Multi_Thread_Repost_Comment import *
import util

#from dao.repost import RepostDao
#from dao.comment import CommentDao
#from PublicToken import PublicToken
#from WeiboClient import WeiboClient
import threading

if __name__ == '__main__':
    params = getParams()
    threadCount = len(params['repostCrawlers'])
    threads = []
    for i in range(0,threadCount):
        athread = threading.Thread(target = crawl_repost_and_comment, args = (i,params))
        threads.append(athread)
    for athread in threads:
        athread.start()
    
    isRunning = True
    while isRunning: 
        isRunning = False
        for athread in threads:
            if athread.isAlive():
                isRunning = True
        
    
    