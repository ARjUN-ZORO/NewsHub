from flask_restful import Api

from .db import db
from .resources import Page

api = Api()

api.add_resource(Page, '/api/latest_news')
