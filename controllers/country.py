from models.Country import Country


def get_all_countries():
    """
    Get list of all records
    """
    all_countries = Country.query.all()
    return all_countries


def add_country(country_name):
    countries = get_all_countries()
    for country in countries:
        if country.name == country_name:
            pass
    else:
        Country.create(name=country_name)
