from bs4 import BeautifulSoup
import urllib
import util
url = 'http://10.197.32.163/Weibo/GetLatestToken'

conn = util.get_crawler_connection()

fp = urllib.urlopen(url)
html_doc = fp.read()
soup = BeautifulSoup(html_doc)

recordlist = soup.body.form.table.find_all('tr');
tokens = []
for i in range(1,len(recordlist)):
    teamID = recordlist[i].find_all('td')[0].contents[0]#'1'
    token = recordlist[i].find_all('td')[2].contents[0]
    isValid = recordlist[i].find_all('td')[3].contents[0]#'1'/'0'
    if teamID == u'1' and isValid == u'1':
        tokens.append(token)
index = 0
#print tokens
cursor = conn.cursor()
cursor.execute('delete from public_token_pool;')
cursor.close()
for token in tokens:
    SQLStatement = '''INSERT INTO `Public_Token_Pool` (`UserID`, `Access_Token`, `TokenStatus`, `TeamID`, `INSERT_TIMESTAMP`, `LAST_UPDATE_TIMESTAMP`) VALUES (%s, '%s', 1, NULL, '0000-00-00 00:00:00', '2012-08-30 07:21:36');
                    '''%(index+19714080000,token)
    cursor = conn.cursor()
    cursor.execute(SQLStatement)
    cursor.close()
    print('token:%s inserted in index:%s'%(token,index))
    index = index + 1

conn.commit()
conn.close()
print('token insert done.')

