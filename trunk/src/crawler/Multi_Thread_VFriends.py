#! -*- coding: utf-8 -*-

import util

from dao.repost import RepostDao
from dao.comment import CommentDao
from PublicToken import PublicToken
from WeiboClient import WeiboClient
from repost import WeiboRepostAPI
from comment import WeiboCommentAPI


def crawl_repost_and_comment(index,params):
    threadCount = len(params['repostCrawlers'])
    statuses = params['statuses']
    statusesCount = len(statuses)
    statusesSlice = statuses[index*statusesCount/threadCount:(index+1)*statusesCount/threadCount]
    repostCrawler = params['repostCrawlers'][index]
    repostDao = params['repostDaos'][index]
    commentCrawler = params['commentCrawlers'][index]
    commentDao = params['commentDaos'][index]
    
    for status in statusesSlice:
        try:
            reposts = repostCrawler.get_reposts_of_status(status[0])
            repostDao.insert_reposts(reposts)
        except Exception, e:
            print ("ERROR: Insert reposts fail: %s" % (str(e), ))
            util.print_full_exception()
        try:
            comments = commentCrawler.get_comments_on_status(status[0])
            commentDao.insert_comments(comments)
        except Exception, e:
            print ("ERROR: Insert comments fail: %s" % (str(e), ))
            util.print_full_exception()


#        reposts = repostCrawler.get_reposts_of_status(status[0])
#        repostDao.insert_reposts(reposts)
#
#        comments = commentCrawler.get_comments_on_status(status[0])
#        commentDao.insert_comments(comments)


def getParams():
    
    params = {}
    
    tokens = PublicToken.getPublicToken()
    singleTokenClients = []
    connections = []
    repostCrawlers = []
    commentCrawlers = []
    repostDaos = []
    commentDaos = []
    for token in tokens:
        client = WeiboClient((token,))
        singleTokenClients.append(client)
        repostCrawlers.append(WeiboRepostAPI(client))
        commentCrawlers.append(WeiboCommentAPI(client))
        try:
            conn = util.get_crawler_connection()
            connections.append(conn)
            repostDaos.append(RepostDao(conn))
            commentDaos.append(CommentDao(conn))
        except Exception, e:
            print ("ERROR: Init conn fail: %s" % (str(e), ))
    params['repostCrawlers'] = repostCrawlers
    params['repostDaos'] = repostDaos
    params['commentCrawlers'] = commentCrawlers
    params['commentDaos'] = commentDaos
    
    try:
        cursor = connections[0].cursor()
        cursor.execute('select id_status from Status') 
        statuses = cursor.fetchall()
        cursor.close()
    except Exception, e:
        print ('Error when load Status from DB')
    print('Load Status from DB done.')
    
    params['statuses'] = statuses    

    return params
        
    


    


