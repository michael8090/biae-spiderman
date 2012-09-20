import types
import MySQLdb
import datetime

gDBHost = 'chn-dilli1'
gDBPort = 3306
gDBUser = 'root'
gDBPassword = 'admin'
gDBSchema = 'biae'
def getConnection():
    try:
        conn = MySQLdb.connect(host=gDBHost, port=gDBPort,
                                   user=gDBUser, passwd=gDBPassword,
                                   db=gDBSchema, charset="utf8")
        return conn
    except Exception, e:
        print ("ERROR: Load EUser fail: %s" % (str(e), ))

#records = ((time,activeness),(...),...)
def isProtential(x,records):
    coverLen = 5
    
    averageActiveness = []
    isProtentialUser = []
    for i in range(coverLen-1):
        averageActiveness.append(None)
        isProtentialUser.append(None)
        
    if type(records) != types.TupleType or len(records) < coverLen:
        print 'invalide input length:%s'%len(records)
        #print 'invalide input length',records
        return None
    
    for i in range(coverLen-1,len(records)):
        Sum = 0
        for j in range(i-(coverLen-1),coverLen-1):
            Sum += records[j][1]
        average = Sum/(coverLen+0.0)
        averageActiveness.append(average)
    
    for i in range(coverLen,len(records)):
        increase = averageActiveness[i] - averageActiveness[i-1]
        if(increase >= x):
            return True
    
    return False

def getUser():
    result = None
    lSQLStatement = 'select distinct(user_id) from fact_user_activeness'
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(lSQLStatement) 
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        
        #print result
        return result
    except Exception, e:
        print ("ERROR: Load EUser fail: %s" % (str(e), ))
        
    return result
def ajustDataFromDB(data):
    indata = list(data)
    for i in range(len(data)-1):
        delt = (indata[i][0] - indata[i-1][0]).days
        if delt > 1:
            for j in range(delt-1):
                dTime = indata[i][0]-datetime.timedelta(j+1)
                indata.insert(i+1+j,(dTime,0))
    return tuple(indata)
            
            
        

def getRecord(user_id):
    result = None
    lSQLStatement = 'select day_date,activeness from fact_user_activeness where user_id=%s order by day_date desc'%user_id
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(lSQLStatement) 
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        #print result
        return ajustDataFromDB(result)
    except Exception, e:
        print ("ERROR: Load EUser fail: %s" % (str(e), ))
        
    return result

def updateDB(records):
    SQLStatement = 'update lu_user set potential_buyer=%s where user_id = %s'
    try:
        conn = getConnection()
        cursor = conn.cursor()
        for record in records:
            SQLs = SQLStatement%(record[1],record[0])
            cursor.execute(SQLs) 
        cursor.close()
        conn.commit()
        conn.close()
        print result
        return result
    except Exception, e:
        print ("ERROR: Load EUser fail: %s" % (str(e), ))

    

def process(x):
    users = getUser()
    result = []
    for user in users:
        user_id = user[0]
        records = getRecord(user_id)
        isP = isProtential(x,records)
        if isP == None:
            continue
        result.append((user_id,isP),)
    return result

if __name__ == '__main__':
    result = process(1)
    print result
    print ('do you want to store this to DB? Y/N')
    answer = input
    if answer == 'y' or answer == 'Y':
        updateDB(result)
        
    