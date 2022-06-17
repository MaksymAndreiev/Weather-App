import doctest

import core

app = core.create_app()


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(core.routes))
    return tests


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)  # разобраться с портом
