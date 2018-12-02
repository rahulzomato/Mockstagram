from mongoengine import *

class Influencers(Document):

	_influencer_id 		= IntField(required = True)
	_name 		  		= StringField(required = True)
	_is_suspicious		= BooleanField(default = False)

	@property
	def influencer_id(self):
		return self._influencer_id

	@influencer_id.setter
	def set_influencer_id(self, influencer_id):
		self._influencer_id = influencer_id


	def get_json(self):
		return {
			"influencer_id": self._influencer_id,
			"name": self._name,
			"_is_suspicious": self._is_suspicious
		}



class InfluencerData(Document):
	influencer			= ReferenceField(Influencers, required = True)
	followers_count 	= IntField()
	following_count 	= IntField()
	update_time			= DateTimeField(required = True)













