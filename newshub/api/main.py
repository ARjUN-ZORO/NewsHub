from flask_restful import Api

from .db import mon_db
from .resources import Page, Page_by_cat, Page_search

api = Api()

api.add_resource(Page, '/api/latest_news')
api.add_resource(Page_by_cat, '/api/news')
api.add_resource(Page_search, '/api/news_find')
