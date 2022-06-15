import re
import psycopg2
from psycopg2._psycopg import AsIs

from core import db


def commit(obj, conn, cur):
    """
    Function for convenient commit
    """
    # db.session.add(obj)
    # db.session.commit()
    # db.session.refresh(obj)
    cur.execute(obj)
    conn.commit()
    cur.close()
    conn.close()
    # return obj


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
        print(table)

        columns = kwargs.keys()
        values = [kwargs[column] for column in columns]
        insert_statement = 'insert into {} (%s) values %s'.format(table)
        print(values)
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
        obj = db.session.query(cls).filter(cls.id == row_id).first()
        db.session.delete(obj)
        db.session.commit()
        if db.session.query(cls).filter(cls.id == row_id).first() is None:
            obj = 1
        else:
            obj = 0
        return obj

    # @classmethod
    # def add_relation(cls, row_id, rel_obj):
    #     """
    #     Add relation to object
    #
    #     cls: class
    #     row_id: record id
    #     rel_obj: related object
    #     """
    #     obj = cls.query.filter_by(id=row_id).first()
    #     if cls.__name__ == 'Actor':
    #         obj.filmography.append(rel_obj)
    #     elif cls.__name__ == 'Movie':
    #         obj.cast.append(rel_obj)
    #     return commit(obj)
    #
    # @classmethod
    # def remove_relation(cls, row_id, rel_obj):
    #     """
    #     Remove certain relation
    #
    #     cls: class
    #     row_id: record id
    #     rel_obj: related object
    #     """
    #     obj = cls.query.filter_by(id=row_id).first()
    #     if cls.__name__ == 'Actor':
    #         obj.filmography.remove(rel_obj)
    #     elif cls.__name__ == 'Movie':
    #         obj.cast.remove(rel_obj)
    #     return commit(obj)
    #
    # @classmethod
    # def clear_relations(cls, row_id):
    #     """
    #     Remove all relations by id
    #
    #     cls: class
    #     row_id: record id
    #     """
    #     obj = cls.query.filter_by(id=row_id).first()
    #     if cls.__name__ == 'Actor':
    #         obj.filmography = []
    #     elif cls.__name__ == 'Movie':
    #         obj.cast = []
    #     return commit(obj)

# def before_insert():
#     pass
#
# func = DDL(
#     "CREATE FUNCTION my_func() "
#     "RETURNS TRIGGER AS $$ "
#     "BEGIN "
#     "NEW.name := 'ins'; "
#     "RETURN NEW; "
#     "END; $$ LANGUAGE PLPGSQL"
# )
#
# trigger = DDL(
#     "CREATE TRIGGER dt_ins BEFORE INSERT ON city "
#     "FOR EACH ROW EXECUTE PROCEDURE my_func();"
# )
#
# event.listen(
#     City,
#     'before_insert',
#     func.execute_if(dialect='postgresql')
# )
#
# event.listen(
#     City,
#     'before_insert',
#     trigger.execute_if(dialect='postgresql')
# )
