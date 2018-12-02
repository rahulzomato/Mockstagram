from mongoengine import connect

mongo = {
	"host": "localhost",
	"port": 27107,
	"database": "mockstagram"
}

CELERY = {
	"BROKER_URL": 'redis://localhost:6379'
}

TASK_ROUTES = {
        'api_crawler'           : {'queue': 'queue_api_crawler'},
        'push_to_api_crawler'      : {'queue': 'queue_push_to_api_crawler'},
    }

INFLUENCER_FETCH_DATA_HOST = "http://localhost:3000"
INFLUENCER_FETCH_DATA_PATH = "/api/v1/influencers/"
INFLUENCER_FETCH_DATA_URL =  INFLUENCER_FETCH_DATA_HOST + INFLUENCER_FETCH_DATA_PATH

INFLUENCER_DATA_UPDATE_FREQUENCY = 1 # minutes

WEBAPP_SERVICE_PORT = 8080
DEBUG = True

connect(mongo['database'])