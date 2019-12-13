import MySQLdb

#按照指定的表内容查找记录
def dbsearch(table,index,value):
    try:
        conn = MySQLdb.connect('localhost','root','root','宾馆住房',charset = 'utf8')
    except:
        print('can\'t connect with MySQL')
    cursor = conn.cursor()

    try:
        cursor.execute("select * from {} where {} = {}".format(table,index,value))
        result = cursor.fetchall()
        return result
    except:
        conn.rollback()
    conn.close()

def dbinsert(table,value):
    try:
        conn = MySQLdb.connect('localhost','root','root','宾馆住房',charset = 'utf8')
    except:
        print('can\'t connect with MySQL')
    cursor = conn.cursor()
    try:
        cursor.execute('insert into {} values {}'.format(table,value))
        cursor.execute()
        return 'insert success'
    except:
        conn.rollback()

dbinsert('clients',('1232421','18856789876'))
print(dbsearch('clients','id','1232421'))