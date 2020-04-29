from flask import Flask


def create_app():
    app = Flask(__name__)
    from newshub.data.scrape_data import scrape
    # print(scrape())
    from newshub.api.db import db
    from newshub.api.settings import SECRET, MONGO_URI, MONGO_DBNAME
    app.config['SECRET_KEY'] = SECRET
    app.config['MONGO_DBNAME'] = MONGO_DBNAME
    app.config['MONGO_URI'] = MONGO_URI
    db.init_app(app)
    from newshub.api.main import api
    api.init_app(app)

    return app
