import re

import psycopg2
from psycopg2._psycopg import AsIs


def commit(obj, conn, cur):
    """
    Function for convenient commit
    """
    cur.execute(obj)
    conn.commit()
    cur.close()
    conn.close()


class Model(object):
    @classmethod
    def create(cls, **kwargs):
        """
        Create new record

        cls: class
        kwargs: dict with object parameters
        """
        conn = psycopg2.connect(user="root", password="root", host="localhost", port="5432",
                                dbname="weather_app")
        cur = conn.cursor()

        class_name = cls.__name__
        class_name = re.sub(r"([A-Z])", r" \1", class_name).split()
        if len(class_name) != 1:
            class_name.insert(1, '_')
        class_name = ''.join(class_name)
        class_name = class_name.lower()
        table = class_name

        columns = kwargs.keys()
        values = [kwargs[column] for column in columns]
        insert_statement = f'insert into {table}(%s) values %s'
        obj = cur.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        return commit(obj, conn, cur)

    @classmethod
    def update(cls, row_id, **kwargs):
        """
        Update record by id

        cls: class
        row_id: record id
        kwargs: dict with object parameters
        """
        conn = psycopg2.connect(user="root", password="root", host="127.0.0.1", port="5432",
                                dbname="weather_app")
        cur = conn.cursor()

        obj = cls.query.filter_by(id=row_id).first()
        keys = kwargs.keys()
        for key in keys:
            exec("obj.{0} = kwargs['{0}']".format(key))
        return commit(obj, conn, cur)

    @classmethod
    def delete(cls, row_id):
        """
        Delete record by id

        cls: class
        row_id: record id
        return: int (1 if deleted else 0)
        """
        conn = psycopg2.connect(user="root", password="root", host="127.0.0.1", port="5432",
                                dbname="weather_app")
        cur = conn.cursor()

        class_name = cls.__name__
        class_name = re.sub(r"([A-Z])", r" \1", class_name).split()
        if len(class_name) != 1:
            class_name.insert(1, '_')
        class_name = ''.join(class_name)
        class_name = class_name.lower()
        table = class_name

        q = f"DELETE FROM {table} WHERE id = {row_id}"
        cur.execute(q)
        conn.commit()
        cur.close()
        conn.close()
