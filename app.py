import os
from flask import Flask, render_template, session, request, redirect, url_for, flash
from extensions import db
from models import User
from forms import LoginForm
from flask_bootstrap import Bootstrap
# 初始化app、扩展
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gl.007@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app)
db.init_app(app)


# 登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    # username = None
    # password = None

    if request.method == 'POST':
        # 匹配数据库用户名和密码
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            redirect(url_for('welcome'))
        else:
            flash('数据错误!!!')
            redirect('login.html')
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/control')
def control():
    pass


if __name__ == '__main__':
    app.run(debug=True)
