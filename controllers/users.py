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


def user_preferences(user_id):
    # get user country id
    conn = psycopg2.connect(user="root", password="root", host="localhost", port="5432",
                            dbname="weather_app")
    cur = conn.cursor()
    postgreSQL_select_Query = f"select country_id from users WHERE id = {user_id}"
    cur.execute(postgreSQL_select_Query)
    country_id = cur.fetchone()[0]
    # get country name (full)
    postgreSQL_select_Query = f"select name from country WHERE id = {country_id}"
    cur.execute(postgreSQL_select_Query)
    country_name = cur.fetchone()
    # get units
    if country_name[0] in countries_codes.keys():
        UserPreferences.create(**{'users_id': user_id, 'measuring_units_id': 3})
    else:
        UserPreferences.create(**{'users_id': user_id, 'measuring_units_id': 2})
    cur.close()
    conn.close()


def set_current_user(id):
    conn = psycopg2.connect(user="root", password="root", host="localhost", port="5432",
                            dbname="weather_app")
    cur = conn.cursor()
    query = f"select * from users where id = {id}"
    cur.execute(query)
    user = cur.fetchone()
    global CURRENT_USER
    CURRENT_USER = user
    cur.close()
    conn.close()


def get_current_user():
    global CURRENT_USER
    return CURRENT_USER

def delete(user_id):
    Users.delete(user_id)
    return redirect('/')
