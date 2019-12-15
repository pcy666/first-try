from flask import Flask
from flask import request
from flask import render_template
import db

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    uname = request.form['username']
    pwd = request.form['password']
    way = request.values.get('options')

    if pwd == db.dbsearch('staff','id',uname)[0][1]:  #判断是否和数据库中的密码一致
        return render_template('signin.html')
    else:
        return render_template('index.html')

@app.route('/ChooseRoom',methods=['POST'])
def ChooseRoom():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()