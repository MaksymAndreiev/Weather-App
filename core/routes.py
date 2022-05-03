from flask import Flask, request
from flask import current_app as app

from controllers.city import add_city as add
from controllers.city import delete as del_


@app.route('/add', methods=['GET', 'POST'])
def add_city():
    add()


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    del_(city_id)
