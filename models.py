# -*- coding: utf-8 -*-
from extensions import db
from datetime import datetime
from flask_login import UserMixin, LoginManager, current_user

login_manager = LoginManager()

# 关联【用户】和【权限】
user_permission = db.Table('user_permission',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.u_id'), primary_key=True),
                           db.Column('permission_id', db.Integer, db.ForeignKey('permission.p_id'), primary_key=True))


@login_manager.user_loader
def load_user(u_id):
    return User.query.get(int(u_id))


# 用户模型
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)  # "id"
    username = db.Column(db.String(20), index=True)  # "用户名"
    password = db.Column(db.String(128))  # "密码"
    real_name = db.Column(db.String(30), index=True)  # 姓名
    department = db.Column(db.String(20), index=True)  # "部门"
    member_since = db.Column(db.DateTime, default=datetime.utcnow())
    permissions = db.relationship('Permission', secondary=user_permission, back_populates='users')

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return self.u_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


# 用户权限
class Permission(db.Model):
    __tablename__ = 'permission'
    p_id = db.Column(db.Integer, primary_key=True)
    p_level = db.Column(db.String(15))
    users = db.relationship('User', secondary=user_permission, back_populates='permissions')

    def __repr__(self):
        return '<Permission %r>' % self.p_level


# 多对多关联表(关联【药品】和【分类】)
drug_category = db.Table('drug_category',
                         db.Column('category_id', db.Integer, db.ForeignKey('category.c_id')),
                         db.Column('drug_id', db.Integer, db.ForeignKey('drug.d_id')))


# 药品模型
class Drug(db.Model):
    __tablename__ = 'drug'
    d_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)  # "序列号"
    d_name = db.Column(db.String(20), unique=True, index=True)  # "名称"
    inventory = db.Column(db.Integer)  # "库存"
    formulation = db.Column(db.String(20), index=True)  # "剂型"
    # variety = db.Column(db.String(20)) # "品种"（暂时使用分类来代替）
    period = db.Column(db.Integer, index=True)  # "有效期：/月"
    about = db.Column(db.Text)  # "关于"
    categories = db.relationship('Category', secondary=drug_category, back_populates='drugs')  # "与【分类】建立双向关系"

    def __repr__(self):
        return '<Drug> %r' % self.d_name


# 分类模型
class Category(db.Model):
    __tablename__ = 'category'
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(20), unique=True)
    level = db.Column(db.String(1))  # ABC分类法
    drugs = db.relationship('Drug', secondary=drug_category, back_populates='categories')  # "与【药品】建立双向关系"

    def __repr__(self):
        return '<Category> %r' % self.c_name



