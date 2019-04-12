# -*- coding: utf-8 -*-
from flask import redirect, url_for
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from models import db, User, Drug, Category, Permission
from extensions import login_manager, current_user
admin = Admin(index_view=AdminIndexView(name='数据中心', template='myadmin/myhome.html', url='/secret'))


@login_manager.user_loader
def load_user(u_id):
    return User.query.get(int(u_id))


# 重写根目录
class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('myadmin/myhome.html')


# ModelView基类
class MyModelView(ModelView):
    column_display_pk = True
    create_modal = True
    page_size = 50

    def is_accessible(self):

        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


# User视图
class UserModelView(MyModelView):
    column_filters = ('username', 'department')
    column_searchable_list = (User.u_id, User.username, User.real_name, User.department)
    column_labels = {'u_id': 'id',
                     'username': '用户名',
                     'password': '密码',
                     'real_name': '真实姓名',
                     'department': '部门',
                     'permissions': '权限',
                     'member_since': '创建日期'}
    # 隐藏密码
    column_exclude_list = ('password',)

    def __init__(self, session, **kwargs):
        super(UserModelView, self).__init__(User, session, **kwargs)


# Permission视图
class PermissionModelView(MyModelView):
    column_labels = {'p_id': 'id',
                     'p_level': '权限等级'}

    def __init__(self, session, **kwargs):
        super(PermissionModelView, self).__init__(Permission, session, **kwargs)


# Drug视图
class DrugModelView(MyModelView):
    column_labels = {'d_id': '药品编号',
                     'd_name': '品名',
                     'inventory': '库存',
                     'formulation': '剂型',
                     'period': '有效期',
                     'about': '关于',
                     'categories': '品类'}
    column_filters = ('d_id', 'd_name', 'inventory', 'formulation', 'period')

    def __init__(self, session, **kwargs):
        super(DrugModelView, self).__init__(Drug, session, **kwargs)


# Category视图
class CategoryModelView(MyModelView):
    column_labels = {'c_id': '分类号',
                     'c_name': '类名',
                     'level': '等级',
                     'drugs': '品名'}

    def __init__(self, session, **kwargs):
        super(CategoryModelView, self).__init__(Category, session, **kwargs)
