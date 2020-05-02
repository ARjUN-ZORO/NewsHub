from flask_restful import Api

from .db import db
from .resources import Page, Page_by_cat

api = Api()

api.add_resource(Page, '/api/latest_news')
api.add_resource(Page_by_cat, '/api/news')
