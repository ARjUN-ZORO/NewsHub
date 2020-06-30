from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from newshub.settings import Config
from flask_admin import Admin

pos_db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin()


login_manager.login_view = "site_bp.login"
# login_manager.login_message_category = "info"

def create_app():
    print('app_name = {}'.format("app"))
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    pos_db.init_app(app)
    from newshub.data.scrape_data import scrape
    login_manager.init_app(app)
    from newshub.site.site_routes import site_bp
    app.register_blueprint(site_bp)

    from newshub.api.db import mon_db, db
    from newshub.api.settings import SECRET, MONGO_URI, MONGO_DBNAME, DEBUG
    app.debug = DEBUG
    app.config['SECRET_KEY'] = SECRET
    app.config['MONGO_DBNAME'] = MONGO_DBNAME
    app.config['MONGO_URI'] = MONGO_URI
    mon_db.init_app(app)
    from newshub.api.main import api
    api.init_app(app)
    admin.init_app(app)
    from flask_admin.contrib.sqla import ModelView
    from newshub.api.models import pagesView
    from newshub.site.models import User
    # admin.add_view(pagesView(db.pages),'Feeds')
    admin.add_view(ModelView(User,pos_db.session))
    return app
