from flask import request, redirect

from models.Users import Users

# на пользователей
# def get_all_users():
#     """
#     Get list of all records
#     """
#     all_users = City.query.all()
#     return all_cities


def add_user():
    login = request.form.get('login')
    # возможно добавить засекречивание пароля
    password = request.form.get('password')
    nickname = request.form.get('nickname')
    # если уже есть такой ник
    country_id = 1
    Users.create(**{'login': login, 'password': password, 'nickname': nickname, 'country_id': country_id})
    return redirect('/')


def delete(user_id):
    Users.delete(user_id)
    return redirect('/')
