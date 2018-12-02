from flask import Flask
from flask_mongoengine import MongoEngine
from healthcheck import HealthCheck

app = Flask(__name__)

db = MongoEngine(app)

health = HealthCheck(app, "/healthcheck")

from .api.influencer import influencer_api
app.register_blueprint(influencer_api)