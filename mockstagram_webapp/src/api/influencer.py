import os, json
from configs import settings as Settings
from models.influencer import Influencers, InfluencerData
from flask import Blueprint, request, url_for, jsonify
from mongoengine import connect


influencer_api = Blueprint('influencer_api', __name__, url_prefix='/api/v1')

@influencer_api.route('/')
def base_route():
	return jsonify(abc="test", status=200)

@influencer_api.route('/influencer/<influencer_id>')
def influencer_details(influencer_id):
	try:
		influencer_id = int(influencer_id)
		influencer = Influencers.objects(_influencer_id = influencer_id).first()
		
		if influencer is None:
			return jsonify(message="Influencer not found", status=404)
		InfDet = InfluencerData.objects(influencer=influencer).order_by('-update_time').first()
		following_ratio = int(InfDet.followers_count/InfDet.following_count) if InfDet.following_count != 0 else InfDet.followers_count
		data = {
			"name": influencer._name,
			"influencer_id": influencer_id,
			"followers_count": InfDet.followers_count,
			"following_count": InfDet.following_count,
			"follower_ratio": , follower_ratio,
			"is_suspicious": influencer._is_suspicious
		}
		return jsonify(
			message="Success",
			status=200,
			data=data
			)

	except ValueError:
		return jsonify(message="Input influencer_id should be integer", status=400)

@influencer_api.route('/influencer/<influencer_id>')
def influencer_details(influencer_id):
	try:
		influencer_id = int(influencer_id)
		influencer = Influencers.objects(_influencer_id = influencer_id).first()
		
		if influencer is None:
			return jsonify(message="Influencer not found", status=404)
		InfDet = InfluencerData.objects(influencer=influencer).order_by('-update_time').first()
		following_ratio = int(InfDet.followers_count/InfDet.following_count) if InfDet.following_count != 0 else InfDet.followers_count
		data = {
			"name": influencer._name,
			"influencer_id": influencer_id,
			"followers_count": InfDet.followers_count,
			"following_count": InfDet.following_count,
			"follower_ratio": follower_ratio,
			"is_suspicious": influencer._is_suspicious
		}
		return jsonify(
			message="Success",
			status=200,
			data=data
			)

	except ValueError:
		return jsonify(message="Input influencer_id should be integer", status=400)


@influencer_api.route('/influencer/rankings')
def influencer_rankings():
	#TODO:  implement ranking logic
	pass
	return jsonify(message="Under construction", status=200)

@influencer_api.route('/influencer/average')
def influencer_average():
	#TODO:  implement average logic
	pass
	return jsonify(message="Under construction", status=200)




@influencer_api.route('/')
def basic_route():
	return jsonify(message="please specify route", status=200)