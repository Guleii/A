# controller.py

from models import db, User, Permission, Drug, Category
from sqlalchemy import desc


class UserDao:
    @staticmethod
    def create_user(username, password, real_name, department):
        new_user = User(username=username, password=password, real_name=real_name, department=department)
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def update_user(user):
        modified_user = User.query.get(user.u_id)
        db.session.commit()

        return modified_user

    @staticmethod
    def delete_user(user):
        user_to_delete = User.query.get(user.u_id)
        db.session.delete(user_to_delete)
        db.session.commit()

        return True

    @staticmethod
    def list_all():
        return User.query.order_by(desc(User.u_id)).all()

    @staticmethod
    def get_user(u_id):
        return User.query.get(u_id)
