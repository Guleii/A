# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required, login_user, logout_user


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()