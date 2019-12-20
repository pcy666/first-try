from flask import Flask
from flask import request
from flask import render_template
from flask import redirect,url_for
import db

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        way = request.values.get('options')
        if pwd == db.dbsearch('staff','id',uname)[0][1]:  #判断是否和数据库中的密码一致
            #判断管理员登录
            if way == 'admin':
                return redirect(url_for('admin',id = uname))
            elif way == 'admin_':
                return redirect(url_for('signin',id = uname))
        else:
            return render_template('index.html')

#普通员工管理网页
@app.route('/signin/<id>', methods=['GET','POST'])
def signin(id):
    #存储可用房间的列表
    single = []
    double = []
    luxury = []
    suite = []
    high = []
    president = []
    for s in db.dbsearch('room','type','单人间'):  #访问数据库，查找所有房间
        if s[2] == 0:  #判断是否有人
            single.append(s)
    for s in db.dbsearch('room','type','双人间'):
        if s[2] == 0:
            double.append(s)
    for s in db.dbsearch('room','type','豪华房'):
        if s[2] == 0:
            luxury.append(s)
    for s in db.dbsearch('room','type','套间'):
        if s[2] == 0:
            suite.append(s)
    for s in db.dbsearch('room','type','高级套间'):
        if s[2] == 0:
            high.append(s)
    for s in db.dbsearch('room','type','总统套房'):
        if s[2] == 0:
            president.append(s)

    if request.method == 'POST':
        type = request.values.get('type')
        if type == '2':
            # 需要从request对象读取表单内容：
            list = request.get_data()
            name = request.values.get('name')
            id = request.values.get('id')
            num = request.values.get('num')
            value = (name,id,num)
            db.dbinsert('clients',value)

            return render_template('signin.html',single = single, double = double,luxury = luxury,suite = suite,high = high,president = president)
        elif type == '4':  #续住
            room_id = request.values.get('roomid')
            days = request.values.get('days')

        elif type == '5':  #房间查询
            room_id = request.values.get('roomid')
        elif type == '6':  #退房
            room_id = request.values.get('roomid')
        else:
            return render_template('signin.html',single = single, double = double,luxury = luxury,suite = suite,high = high,president = president)
    elif request.method == 'GET':
        return render_template('signin(1).html',single = single, double = double,luxury = luxury,suite = suite,high = high,president = president)
    
#管理员网页
@app.route('/admin/<id>',methods=['GET','POST'])
def admin(id):
    if request.method == 'GET':
        single = db.dbsearch('room','type','单人间')[0][1]
        double = db.dbsearch('room','type','双人间')[0][1]
        luxury = db.dbsearch('room','type','豪华房')[0][1]
        suite = db.dbsearch('room','type','套间')[0][1]
        high = db.dbsearch('room','type','高级套间')[0][1]
        president = db.dbsearch('room','type','总统套房')[0][1]
        staff = db.dbsearchAll('staff','*')
        return render_template('admin.html',single = single, double = double,luxury = luxury,suite = suite,high = high,president = president,staff = staff)
    elif request.method == 'POST':
        num = request.values.get('num')
        type = request.values.get('type')  #功能位，决定使用的功能
        newkey =request.values.get('newkey')
        uname =request.values.get('uname')
        psw =request.values.get('psw')
        price =request.values.get('price')
        #房间种类 num
        if type == '1': #修改房间价格
            if num == '1':
                db.dbchangeOneNum('room','type','单人间','price',int(price))
            elif num == '2':
                db.dbchangeOneNum('room','type','双人间','price',int(price))
            elif num == '3':
                db.dbchangeOneNum('room','type','豪华房','price',int(price))
            elif num == '4':
                db.dbchangeOneNum('room','type','套间','price',int(price))
            elif num == '5':
                db.dbchangeOneNum('room','type','高级套间','price',int(price))
            elif num == '6':
                db.dbchangeOneNum('room','type','总统套房','price',int(price))
        elif type == '2': #修改密码
            db.dbchangeOneNum('staff','id',num,'pwd',newkey)
        elif type == '3': #删除管理员账户
            db.dbDelete('staff','id',uname)

@app.route('/ChooseRoom',methods=['POST'])
def ChooseRoom():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()