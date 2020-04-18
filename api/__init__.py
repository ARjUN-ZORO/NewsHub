from flask import Flask
from flask_mongoalchemy import MongoAlchemy

api_app = Flask(__name__)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['MONGOALCHEMY_DATABASE'] = 'newshub'
# app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://<user_name>:<password>@ds143932.mlab.com:43932/newshub'

db = MongoAlchemy(api_app)

from newshub.api import routes
