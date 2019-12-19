from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
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
                #此处最好使用url_for()
                return redirect('/admin')
            elif way == 'admin_':
                return redirect('/signin')
                # return render_template('signin.html')
        else:
            return render_template('index.html')

#普通员工管理网页
@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        # 需要从request对象读取表单内容：
        status = request.values.get('status')  #用于判断用户当前处在的状态
        if status == '2':
            uname = request.form['guest_name']
            uid = request.form['guest_id']
            unum = request.form['guest_num']
            value = (uname,uid,unum)
            db.dbinsert('clients',value)
            return render_template('signin 2.html')
        else:
            return render_template('signin.html')
    elif request.method == 'GET':
        return render_template('signin.html')
    
#管理员网页
@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')
    elif request.method == 'POST':
        num = request.values.get('num')
        type = request.values.get('type')
        newkey =request.values.get('newkey')
        uname =request.values.get('uname')
        psw =request.values.get('psw')
        price =request.values.get('price')
        #房间种类 num
        # if type == '1': #修改房间价格
        # elif type == '2': #修改密码
        # elif type == '3': #删除管理员账户
        return render_template('index.html')

@app.route('/ChooseRoom',methods=['POST'])
def ChooseRoom():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()