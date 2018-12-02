import requests, json, datetime
from mongoengine import *
from celery import Celery
from celery.schedules import crontab
from configs import settings as Settings
from celery.utils.log import get_task_logger
from models.influencer import Influencers, InfluencerData
from mockstagram_crawler.src.api_crawler import API_Crawler

celery = Celery(broker = Settings.CELERY['BROKER_URL'])
celery.conf.task_routes = Settings.TASK_ROUTES

logger = get_task_logger(__name__)

connect(Settings.mongo["database"])


@celery.on_after_configure.connect
def push_to_api_crontab(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/'+str(Settings.INFLUENCER_DATA_UPDATE_FREQUENCY)),
                             push_to_api_crawler.s().apply_async())

# this method will contain logic of push 
# @celery.task(name='push_to_api_crawler')
def push_to_api_crawler():	
	# returns a pointer to db
	all_influencers = Influencers.objects.all()

	for influencer in list(all_influencers):
		task = API_Crawler()
		task.delay(influencer.to_json())
		
