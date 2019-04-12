# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import login_user
from extensions import db, migrate, login_manager, logout_user
from models import User
from forms import LoginForm
from flask_bootstrap import Bootstrap
from views import admin, MyHomeView, UserModelView, PermissionModelView, DrugModelView, CategoryModelView,AdminIndexView
from flask_babelex import Babel

# 初始化app、扩展
app = Flask(__name__)

# flask-bable
bable = Babel(app)

# APP CONFIG
app.config['BABLE_DEFAULT_LOCALE'] = 'zh_CN'
app.config['SECRET_KEY'] = 'hard to guess'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gl.007@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# flask-bootstrap
bootstrap = Bootstrap(app)

# flask-sqlalchemy
db.init_app(app)

# flask-migrate
migrate.init_app(app, db)

# flask-login
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = '请登录!'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

# flask-admin
admin.name = '后台管理系统'
admin.template_mode = 'bootstrap3'
admin.init_app(app)


admin.add_view(UserModelView(db.session, name='用户管理'))
admin.add_view(PermissionModelView(db.session, name='权限管理'))
admin.add_view(DrugModelView(db.session, name='药品管理'))
admin.add_view(CategoryModelView(db.session, name='药品分类'))




# 本地化语言
@bable.localeselector
def get_locale():
    override = 'zh_CN'
    if override:
        session['lang'] = override
    return session.get('lang', 'en')


# 登录页面
@app.route('/', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 匹配数据库用户名和密码
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is not None and user.password == form.password.data:
            login_user(user)
            return redirect('/secret')
        else:
            flash('用户名或密码错误，请重新输入！')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return 'logged out'

# @app.route('/secret')
# @login_required
# def secret():
#
#     return render_template('myadmin/myhome.html')


# 待删除
@app.route('/control')
def control():
    return render_template('base_control.html')


# 搜索药品
@app.route('/drug_search', methods=['GET', 'POST'])
def drug_search():
    return render_template('drug_search.html')


# 管理药品
@app.route('/drug_manager', methods=['GET', 'POST'])
def drug_manager():
    return render_template('drug_manager.html')


# 管理账户
@app.route('/admin_manager')
def admin_manager():
    return render_template('admin_manager.html')


if __name__ == '__main__':
    app.run(debug=True)
