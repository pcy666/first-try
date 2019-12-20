from flask import Flask
from flask import request
from flask import render_template
from flask import redirect,url_for,jsonify
import datetime
import db
import json

app = Flask(__name__)

name = ''
id = ''
num = ''

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
                return redirect(url_for('admin'))
            elif way == 'admin_':
                return redirect(url_for('signin'))
        else:
            return render_template('index.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
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

    if request.method == 'GET':
        return render_template('signin.html',single = single, double = double,luxury = luxury,suite = suite,high = high,president = president)

    elif request.method == 'POST':
        # 需要从request对象读取表单内容：
        name = request.values.get('name')
        id = request.values.get('id')
        num = request.values.get('num')
        value = (name,id,num)
        db.dbinsert('clients',value)
        return render_template('signin.html',single = single, double = double,luxury = luxury,suite = suite,high = high,president = president)

@app.route('/admin/',methods=['GET','POST'])
def admin():
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
        return render_template('admin.html')

@app.route('/ChooseRoom',methods=['POST'])
def ChooseRoom():
    a = request.get_data()

    print(a)
    return "恭喜入住成功,祝旅途愉快"

@app.route('/guestinfo',methods=['POST'])
def guestinfo():
    global name,id,num
    name = request.values.get('name')
    id = request.values.get('id')
    num = request.values.get('num')
    value = (name,id,num)
    db.dbinsert('clients',value)
    print(name,id,num)
    return('提交数据成功')

@app.route('/continue',methods=['POST'])
def livelonger():
    room_id = request.values.get('roomid')
    days = request.values.get('days')
    room = db.dbsearch('cl_in_room','room_id',room_id)
    if room[0][5] == '':
        room[0][5] = datetime.datetime.today()
    time = room[0][5] + datetime.timedelta(int(days))
    db.dbchangeOneNum('cl_in_room','room_id',room_id,'time_out',time)
    print(room_id,days)
    return('提交数据成功')

@app.route('/checkout',methods=['POST'])
def checkout():
    room_id = request.values.get('roomid')
    room = db.dbsearch('cl_in_room','room_id',room_id)
    flag = db.dbsearch('room','room_id',room_id)
    data={
        'ddnum':room[0][0],
        'idnum':room[0][1],
        'room_num':[0][2],
        'reservetime':[0][3],
        'moveintime':[0][4],
        'checkouttime':[0][5],
        'pay':flag[0][1]
    }
    db.dbDelete('cl_in_room','room_id',room_id)
    return jsonify(data)

@app.route('/search',methods=['POST'])
def search():
    room_id = request.values.get('roomid')
    room = db.dbsearch('cl_in_room','room_id',room_id)
    flag = db.dbsearch('room','room_id',room_id)
    TimeIn = room[0][4]
    TimeOut = room[0][5]
    data = {'RoomNum':room_id,
    'Flag' : flag,
    'TimeIn': TimeIn,
    'TimeOut' : TimeOut}
    return jsonify(data)

if __name__ == '__main__': 
    app.run()
