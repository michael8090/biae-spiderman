'''Connection fetching methods for Weibo API
'''
import urllib2
import json
import time
import types

class WeiboClient():
    #limited 5 calls per 20 seconds, = 900 calls per hour
    CALL_TIMES_PER_INTERVAL = 5
    PERIOD_INTERVAL_SECONDS = 20
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

    
    mBasicURL = 'https://api.weibo.com/2/%s.json?'
    mPublicToken = [];
    #mTokenUsedTimeList is a map {'token owner uid', [time1, time2, time3...]}
    mTokenUsedTimeList = {};
    
    #only use the first row of public token fetched
    def __init__(self, iPublicToken):
        self.mPublicToken = iPublicToken;
    
    #composite the API name and parameters into a URL
    def _getAPICallURL(self, iAPI, iParams):
        lURL = self.mBasicURL % (iAPI)
        for (lKey, lValue) in iParams.iteritems():
            lParamString = "%s=%s&" % (lKey, lValue)
            lURL += lParamString
        #print(lURL[:-1])
        print '.',
        return lURL[:len(lURL) - 1]
    
 #support the sleep and re-try   
    def _getPage(self,lURL):
        try:
            self._controlCallTypeFrequency()
            req = urllib2.Request(lURL)
            response = urllib2.urlopen(req,timeout=8)
            page = response.read()
            response.close()
            return page
        except urllib2.URLError, e:
            if(str(e) == '<urlopen error timed out>'):
                for i in range(0,3):
                    try:
                        self._controlCallTypeFrequency()
                        req = urllib2.Request(lURL)
                        response = urllib2.urlopen(req,timeout=8)
                        page = response.read()
                        response.close()
                        return page
                    except urllib2.URLError, e1:
                        print('retry %d failed in 3 retries'%(i+1))
            raise
        



    #fetch the API with multiple pages and cursor parameters
    def _fetchMultiplePages(self, iAPI, iParams):
        if self.mPagingAPIs[iAPI] == 'cursor':
            iParams['cursor'] = 0
            oJsonResult = []
            while True:
                lURL = self._getAPICallURL(iAPI, iParams)
                try:
                    page = self._getPage(lURL) 
                    lJsonResult = json.loads(page)
                    oJsonResult += lJsonResult[self.mAPIDataFields[iAPI]]
                    lNextCursor = lJsonResult['next_cursor']
                    if lNextCursor == 0:
                        return oJsonResult
                    iParams['cursor'] = lNextCursor
                except urllib2.HTTPError, e:
                    print ('Page: \n\tError: The server couldn\'t fulfill the request. Error code: %s' % (str(e)))
        elif self.mPagingAPIs[iAPI] == 'page':
            #print 'to be continued...'
            iParams['page'] = 1
            oJsonResult = []
            while True:
                lURL = self._getAPICallURL(iAPI, iParams)
                try:
                    page = self._getPage(lURL)
                    #print(page)
                    lJsonResult = json.loads(page)
                    oJsonResult += lJsonResult[self.mAPIDataFields[iAPI]]
                    totalNumber = lJsonResult['total_number']
                    currentPage = iParams['page']
                    if currentPage*50 >= totalNumber:
                        return oJsonResult
                    iParams['page'] = currentPage+1
                except urllib2.HTTPError, e:
                    print ('Page: \n\tError: The server couldn\'t fulfill the request. Error code: %s' % (str(e)))


        return {'error': 'unknown fetch type'}
    
    #fetch the API with single page
    def _fetchSinglePage(self, iAPI, iParams):
        lURL = self._getAPICallURL(iAPI, iParams)
        try:
            page = self._getPage(lURL)
            oJsonResult = json.loads(page)
            return oJsonResult
        except urllib2.HTTPError, e:
            print ('Page: \n\tError: The server couldn\'t fulfill the request. Error code: %s' % (str(e)))

    #control call weibo API server's frequency so that won't exceed the fetch limitation
    def _controlCallTypeFrequency(self):
        while(True):
            lNow = time.time()
            #mPublicToken is a list:['uid', 'access_token']
            lTokenOwner = self.mPublicToken[0]
            #the token has never been used before:
            if not self.mTokenUsedTimeList.has_key(lTokenOwner):
                #initial with empty time list 
                self.mTokenUsedTimeList[lTokenOwner] = []
            #the token has not been used more than 5 times ever:
            elif len(self.mTokenUsedTimeList[lTokenOwner]) < self.CALL_TIMES_PER_INTERVAL:
                self.mTokenUsedTimeList[lTokenOwner].append(lNow)
            else:
                assert(len(self.mTokenUsedTimeList[lTokenOwner]) == self.CALL_TIMES_PER_INTERVAL)
                lTimeDiff = lNow - self.mTokenUsedTimeList[lTokenOwner][0]
                #the token has been used more than 5 times in 20 seconds, need wait here
                if lTimeDiff <= self.PERIOD_INTERVAL_SECONDS:
                    time.sleep(self.PERIOD_INTERVAL_SECONDS + 1 - lTimeDiff) 
                    continue
                #the token has not been used more than 5 times in 20 seconds
                else:
                    self.mTokenUsedTimeList[lTokenOwner].pop(0)
                    self.mTokenUsedTimeList[lTokenOwner].append(lNow)
            return
    
    #fetch the connection with given API name and parameters
    def fetchUsingAPI(self, iAPI, iParams):
        #self._controlCallTypeFrequency()
        oJsonResult = {}
        if self.mPagingAPIs.has_key(iAPI):
            oJsonResult = self._fetchMultiplePages(iAPI, iParams)
        else:
            oJsonResult = self._fetchSinglePage(iAPI, iParams)
            
        assert type(oJsonResult) == types.ListType or type(oJsonResult) == types.DictType
        if type(oJsonResult) == types.DictType and oJsonResult.has_key('error'):
            if oJsonResult['error'] == 'expired_token' or oJsonResult['error'] == 'invalid_access_token':
                #write back to public token pool with invalid token mark
                print 'access token expired or invalid!'
        return oJsonResult
