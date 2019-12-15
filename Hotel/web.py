from flask import Flask
from flask import request
from flask import render_template
import db

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        # 需要从request对象读取表单内容：
        status = request.values.get('status')
        if status == '2':
            uname = request.form['guest_name']
            uid = request.form['guest_id']
            unum = request.form['guest_num']
            value = (uname,uid,unum)
            db.dbinsert('clients',value)
            return render_template('signin 2.html')
        else:
            uname = request.form['username']
            pwd = request.form['password']
            way = request.values.get('options')

            if pwd == db.dbsearch('staff','id',uname)[0][1]:  #判断是否和数据库中的密码一致
                return render_template('signin.html')
            else:
                return render_template('index.html')
    elif request.method == 'GET':
        return render_template('signin.html')
    


@app.route('/ChooseRoom',methods=['POST'])
def ChooseRoom():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()