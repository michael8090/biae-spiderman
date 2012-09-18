'''Connection fetching methods for Weibo API
'''
import urllib2
import json
import time
import types
import util
import threading
import random
from math import *

#paging or cursor fetch is supported for such API
mPagingAPIs = {'statuses/friends_timeline':             'page', \
               'statuses/home_timeline':                'page', \
               'statuses/user_timeline':                'page', \
               'comments/timeline':                     'page', \
               'comments/show':                         'page', \
               'statuses/repost_timeline':              'page', \
               'friendships/friends/in_common':         'page', \
               'friendships/friends/bilateral':         'page', \
               'friendships/friends/bilateral/ids':     'page', \
                'friendships/friends_chain/followers':  'page', \
                'suggestions/users/may_interested':     'page', \
                'friendships/friends':                  'cursor', \
                'friendships/followers':                'cursor', \
                'friendships/friends/ids':              'cursor', \
                'friendships/followers/ids':            'cursor'}

#the data field name for fetch json returned
mAPIDataFields = {'statuses/friends_timeline':          'statuses', \
                'statuses/home_timeline':               'statuses', \
                'statuses/user_timeline':               'statuses', \
                'comments/timeline':                    'comments', \
                'comments/show':                        'comments', \
                'statuses/repost_timeline':             'reposts', \
                'friendships/friends/in_common':        'users', \
                'friendships/friends/bilateral':        'users', \
                'friendships/friends_chain/followers':  'users', \
                'friendships/followers/active':         'users', \
                'friendships/friends':                  'users', \
                'friendships/followers':                'users', \
                'friendships/friends/ids':              'ids', \
                'friendships/friends/bilateral/ids':    'ids', \
                'friendships/followers/ids':            'ids'}
# basic URL
basicURL = 'https://api.weibo.com/2/%s.json?'

#global list for monitoring usage of each token
tokenUsedTimeList = {};

#limited 5 calls per 20 seconds, = 900 calls per hour per token
CALL_TIMES_PER_INTERVAL = 5
PERIOD_INTERVAL_SECONDS = 20

class WeiboClient():

    
    #token load balance 
    def getBalancedToken(self):
        self.publicLock.acquire()
        i = self.currentUsedTokenIndex
        if i == None:
            i = random.randrange(len(self.mPublicToken))
        else:
            i = i+1
        if i >= len(self.mPublicToken):
            i = 0
#        i = random.randrange(len(self.mPublicToken))
        self.currentUsedTokenIndex = i
        self.publicLock.release()
        return self.mPublicToken[i][1]

        
    
    #only use the first row of public token fetched
    def __init__(self, iPublicToken):
        self.mPublicToken = iPublicToken;
        self.tokenLocks = {}
        for tokenRecord in iPublicToken:
            token = tokenRecord[1]
            lock = threading.Lock()
            self.tokenLocks[token] = lock
            
        self.publicLock = threading.Lock()
        #tokenUsedTimeList is a map {'token owner uid', [time1, time2, time3...]}
        self.currentUsedTokenIndex = None
        self.retryTimes = 10
        self.timeOut = 30
        self.pageCount = 100
        self.maxTotalNumber = 5000
    
    #composite the API name and parameters into a URL
    def _getAPICallURL(self, iAPI, iParams):
        token = self.getBalancedToken()
        iParams['access_token'] = token
        
        lURL = basicURL % (iAPI)
        for (lKey, lValue) in iParams.iteritems():
            lParamString = "%s=%s&" % (lKey, lValue)
            lURL += lParamString
        #print(lURL[:-1])
        return lURL[:-1]
    
#support the sleep and re-try   
    def _getPage(self,lURL):

        for i in range(0,self.retryTimes):
            try:
                self._controlCallTypeFrequency(lURL)
                req = urllib2.Request(lURL)
                response = urllib2.urlopen(req,timeout=self.timeOut)
                page = response.read()
                response.close()
                #print(chardet.detect(page))
                page = util.remove_InvalideChar_utf8(page)
                #print(page)
                return page
            except urllib2.URLError, e:
                if(str(e) == '<urlopen error timed out>'):
                    print('Server response time out, retrying...%d in %d'%(i+1,self.retryTimes))
                    continue
                else:
                    print('Error in _getPage,the returned page is :%s  URL:%s'%(page,lURL))
                    raise e
        if i == self.retryTimes:
            print ('All the retries failed. Retried URL%s'%lURL)

    #fetch data and return (page_count, total_number)
    def _fetchData(self,lURL,oJsonResult,iAPI):
            try:
                #print lURL
                page = self._getPage(lURL) 
                lJsonResult = json.loads(page)
                resultList = lJsonResult[mAPIDataFields[iAPI]]
                #print 'page count:'+str(len(resultList))
                self.publicLock.acquire()
                oJsonResult += resultList
                self.publicLock.release()
                return (len(resultList),lJsonResult['total_number'])
            except urllib2.HTTPError, e:
                print ('Error when getting Data in _fetchData: %s  URL:%s' % (str(e),lURL))
        
    # Cursor calls
    def _fetchCursorCall(self, iAPI, iParams):
        iParams['count'] = self.pageCount
        iParams['cursor'] = 0
        oJsonResult = []
        current_cursor = 0
        
        #get total number
        lURL = self._getAPICallURL(iAPI, iParams)
        try:
            (page_count,total_number) = self._fetchData(lURL, oJsonResult, iAPI)
        except urllib2.HTTPError, e:
            print ('Error when trying to get total number in Cursor calls: %s  URL:%s' % (str(e),lURL))
        
        threads = []    
        for current_cursor in range(iParams['count'],min(total_number,self.maxTotalNumber),iParams['count']):
            iParams['cursor'] = current_cursor
            lURL = self._getAPICallURL(iAPI, iParams)
            athread = threading.Thread(target = self._fetchData,args = (lURL, oJsonResult, iAPI))
            threads.append(athread)
            athread.start()
            
        #wait till all threads finish
        util.wait_for_threads(threads)
        return oJsonResult
    # Page calls
    def _fetchPageCall(self, iAPI, iParams):
        iParams['count'] = self.pageCount
        iParams['page'] = 1
        oJsonResult = []
        
        #get total number
        lURL = self._getAPICallURL(iAPI, iParams)
        try:
            (page_count,total_number) = self._fetchData(lURL, oJsonResult, iAPI)
        except urllib2.HTTPError, e:
            print ('Error when trying to get total number in Cursor calls: %s  URL:%s' % (str(e),lURL))
           
        threads = []    
        for currentPage in range(2,int(min(ceil(total_number/iParams['count']),ceil(self.maxTotalNumber/iParams['count'])))+1):
            iParams['page'] = currentPage
            lURL = self._getAPICallURL(iAPI, iParams)
            athread = threading.Thread(target = self._fetchData,args = (lURL, oJsonResult, iAPI))
            threads.append(athread)
            athread.start()
        #wait till all threads finish    
        util.wait_for_threads(threads)
        return oJsonResult

    #fetch the API with multiple pages and cursor parameters
    def _fetchMultiplePages(self, iAPI, iParams):
        if mPagingAPIs[iAPI] == 'cursor':
            #if not iParams.has_key('count'):
            return self._fetchCursorCall(iAPI, iParams)

                    
        elif mPagingAPIs[iAPI] == 'page':
            return self._fetchPageCall(iAPI, iParams)
        else:
            return {'error': 'unknown fetch type'}
    
    #fetch the API with single page
    def _fetchSinglePage(self, iAPI, iParams):
        lURL = self._getAPICallURL(iAPI, iParams)
        try:
            page = self._getPage(lURL)
            oJsonResult = json.loads(page)
            return oJsonResult
        except urllib2.HTTPError, e:
            print ('Error in _fetchSinglePage: %s  URL:%s' % (str(e),lURL))
            
    #get token from URL
    def _getTokenFromURL(self,URL):
        index = URL.find('access_token')
        if index == -1:
            print 'invalid URL'
            return None
        token = ''
        for i in range(index+len('access_token='),len(URL)):
            if URL[i]=='&':
                break;
            else:
                token += URL[i]
        return token
        
    #control call weibo API server's frequency so that won't exceed the fetch limitation
    def _controlCallTypeFrequency(self,URL):
        token = self._getTokenFromURL(URL)
        if token == None:
            return
        self.tokenLocks[token].acquire()
        global tokenUsedTimeList
        while(True):
            lNow = time.time()
            #mPublicToken is a list:['uid', 'access_token']
#            lTokenOwner = self.mPublicToken[self.currentUsedTokenIndex][1]
            #lTokenOwner = 'the_only_owner'
            #the token has never been used before:
            if not tokenUsedTimeList.has_key(token):
                #initial with empty time list 
                tokenUsedTimeList[token] = []
            #the token has not been used more than 5 times ever:
            elif len(tokenUsedTimeList[token]) < CALL_TIMES_PER_INTERVAL:
                tokenUsedTimeList[token].append(lNow)
            else:
                assert(len(tokenUsedTimeList[token]) == CALL_TIMES_PER_INTERVAL)
                lTimeDiff = lNow - tokenUsedTimeList[token][0]
                #the token has been used more than 5 times in 20 seconds, need wait here
                if lTimeDiff <= PERIOD_INTERVAL_SECONDS:
                    time.sleep(PERIOD_INTERVAL_SECONDS + 1 - lTimeDiff) 
                    continue
                #the token has not been used more than 5 times in 20 seconds
                else:
                    tokenUsedTimeList[token].pop(0)
                    tokenUsedTimeList[token].append(lNow)
            self.tokenLocks[token].release()
            return
    
    #fetch the connection with given API name and parameters
    def fetchUsingAPI(self, iAPI, iParams):
        #self._controlCallTypeFrequency()
        oJsonResult = {}
        if mPagingAPIs.has_key(iAPI):
            oJsonResult = self._fetchMultiplePages(iAPI, iParams)
        else:
            oJsonResult = self._fetchSinglePage(iAPI, iParams)
            
        assert type(oJsonResult) == types.ListType or type(oJsonResult) == types.DictType
        if type(oJsonResult) == types.DictType and oJsonResult.has_key('error'):
            if oJsonResult['error'] == 'expired_token' or oJsonResult['error'] == 'invalid_access_token':
                #write back to public token pool with invalid token mark
                print 'access token expired or invalid!'
        return oJsonResult
