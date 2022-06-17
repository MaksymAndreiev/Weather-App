import core

app = core.create_app()


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)  # разобраться с портом
