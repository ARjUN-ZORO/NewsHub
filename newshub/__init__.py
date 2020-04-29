from flask import Flask


def create_app():
    app = Flask(__name__)
    from newshub.data.scrape_data import scrape
    print(scrape())
    return app
