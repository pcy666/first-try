import MySQLdb

#按照指定的表内容查找记录
def dbsearch(table,index,value):
    try:
        conn = MySQLdb.connect('localhost','root','root','宾馆住房',charset = 'utf8')
    except:
        print('can\'t connect with MySQL')
        return 0
    cursor = conn.cursor()
    try:
        cursor.execute("select * from {} where {} = \'{}\'".format(table,index,value))
        result = cursor.fetchall()
        return result
    except:
        conn.rollback()
        return 0
    conn.close()

def dbsearchAll(table,target):
    try:
        conn = MySQLdb.connect('localhost','root','root','宾馆住房',charset = 'utf8')
    except:
        print('can\'t connect with MySQL')
        return 0
    cursor = conn.cursor()
    try:
        cursor.execute("select {} from {}".format(target,table))
        result = cursor.fetchall()
        return result
    except:
        conn.rollback()
        return 0
    conn.close()

def dbinsert(table,value):
    try:
        conn = MySQLdb.connect('localhost','root','root','宾馆住房',charset = 'utf8')
    except:
        print('can\'t connect with MySQL')
        return 0
    cursor = conn.cursor()
    try:
        cursor.execute('insert into {} values {}'.format(table,value))
        cursor.execute()
        return 'insert success'
    except:
        conn.rollback()
        return 0

def dbDelete(table,target,value):
    try:
        conn = MySQLdb.connect('localhost','root','root','宾馆住房',charset = 'utf8')
    except:
        print('can\'t connect with MySQL')
        return 0
    cursor = conn.cursor()
    try:
        cursor.execute("delete from {} where {} = \'{}\'".format(table,target,value))
        cursor.execute()
        return 'delete success'
    except:
        conn.rollback()
        return 0


def dbchangeOneNum(table,attr,attr_value,attr_change,change_value):
    try:
        conn = MySQLdb.connect('localhost','root','root','宾馆住房',charset = 'utf8')
    except:
        print('can\'t connect with MySQL')
        return 0
    cursor = conn.cursor()
    try:
        cursor.execute("update {} set {}=\'{}\' where {}=\'{}\'".format(table,attr_change,change_value,attr,attr_value))
        cursor.execute()
        return True
    except:
        conn.rollback()
        return 0

if __name__ == "__main__":
    data = "('601','6000','0','总统套房')"
    dbinsert('room',data)