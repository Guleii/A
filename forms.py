from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


# 登录表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


# 添加用户
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    username = StringField('Username', validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('Password', validators=[DataRequired])
    password2 = PasswordField('Confirm password', validators=[DataRequired, EqualTo(password, '两次密码输入应相同')])
    submit = SubmitField('submit')


# 查询用户
class SelectUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 30)])
    id = StringField('Id', validators=[DataRequired(), Length(1, 30)])


# 添加药品
class CreateDrug(FlaskForm):
    pass
