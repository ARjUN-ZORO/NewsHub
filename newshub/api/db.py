from flask_pymongo import PyMongo
import pymongo
# from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
# from flask import current_app as app

# mdb = MongoEngine(app)
mon_db = PyMongo()
# app.session_interface=MongoEngineSessionInterface(mdb)

conn = pymongo.MongoClient()
db = conn.nh
