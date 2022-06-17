import psycopg2
from models.Country import Country


def get_all_countries():
    """
    Get list of all records
    """
    conn = psycopg2.connect(user="root", password="root", host="127.0.0.1", port="5432",
                            dbname="weather_app")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM county")
    all_countries = [r[0] for r in cur.fetchall()]
    # all_countries = Country.query.all()
    return all_countries


def add_country(country_name):
    """
    Adds a non-duplicate country

    :param country_name: country name
    """
    countries = get_all_countries()
    for country in countries:
        if country.name == country_name:
            pass
    else:
        Country.create(name=country_name)
