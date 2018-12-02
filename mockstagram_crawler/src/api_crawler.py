import requests, json, datetime
from mongoengine import *
from celery import Celery
from celery.schedules import crontab
from configs import settings as Settings
from celery.utils.log import get_task_logger
from models.influencer import Influencers, InfluencerData

celery = Celery(broker = Settings.CELERY['BROKER_URL'])
celery.conf.task_routes = Settings.TASK_ROUTES

logger = get_task_logger(__name__)

# this method will crawl the data.

@celery.on_after_configure.connect
def push_to_api_crontab(sender, **kwargs):
    #sender.add_periodic_task(crontab(minute=Settings.INFLUENCER_DATA_UPDATE_FREQUENCY),
     #                        push_to_api_crawler.s().apply_async())

    sender.add_periodic_task(60.0, push_to_api_crawler.s(), name='push to api crawler')


@celery.task(name='push_to_api_crawler')
def push_to_api_crawler():

	# task = API_Crawler()
	# task.delay('test')

	connect(Settings.mongo["database"])
	all_influencers = Influencers.objects.all()

	for influencer in list(all_influencers):
		task = API_Crawler()
		task.delay(influencer.influencer_id)


class API_Crawler(celery.Task):
	name = "api_crawler"

	def run(self, influencer):
		# influencer_id = influencer.get("influencer_id")
		url = Settings.INFLUENCER_FETCH_DATA_URL + str(influencer)
		print(url)
		req = requests.get(url)
		response_code = req.status_code
		return {
			"data": req.content,
			"response_code": response_code
			}	

	def on_success(self, retval, task_id, args, kwargs):
		
		if retval.get("response_code") == 200:
			connect(Settings.mongo["database"])
			data = json.loads(retval.get("data"))
			logger.info("Successfully crawled. Saving to database.")

			influencer = Influencers.objects(_influencer_id=data.get("pk")).first()
			inf_data = InfluencerData()
			inf_data.influencer = influencer
			inf_data.followers_count = data.get("followerCount")
			inf_data.following_count = data.get("followingCount")
			inf_data.update_time = datetime.datetime.now()
			inf_data.save()

		else:
			logger.info("Unable to crawl" + str(task_id))


	def on_failure(self, exc, task_id, args, kwargs, einfo):
		logger.info("Something went wrong. Unable to crawl.")
		# log the influencer_id and send back to push_to_api_crawler again.


celery.tasks.register(API_Crawler)



# this method will crawl the data.
# @celery.task(name = "api_crawler")
# def API_Crawler(influencer):
# 	# send to parser to generate arguments
# 	influencer_id = influencer.get("influencer_id")
# 	url = Settings.INFLUENCER_FETCH_DATA_URL + str(influencer_id)
# 	print(url)
# 	req = requests.get(url)
# 	response_code = req.status_code
# 	print({
# 		"data": req.content,
# 		"response_code": response_code
# 		})	
