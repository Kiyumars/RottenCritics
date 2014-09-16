import sys
import os
import logging
import random
import json
import urllib2
from bson.objectid import ObjectId

import tornado.ioloop
import tornado.web
import tornado.autoreload

from rottentomatoes import RT
import imdb
from pymongo import MongoClient

imd = imdb.IMDb()
rt = RT()
client = MongoClient()
db = client.mydb



class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("home.html", title='title' )


class GameHandler(tornado.web.RequestHandler):
	def get(self):
		players = create_player_dict(self.get_argument('players'))
		game_id = start_game_session(players)

		actor_name = self.get_argument('actor_entered')
		actor_db_entry = is_actor_in_actors_db(actor_name)

		if not actor_db_entry:
			Actor = get_actor_object_from_imdb(actor_name)
			misspelled_name = is_actor_in_actors_db(Actor['name'])
			
			if misspelled_name:
				movie_list = misspelled_name
				movie = movie_list.pop(random.randint(0, len(movie_list) - 1))
				push_movies_from_actorDB_to_gameSessionsDB(game_id, movie_list, movie)
				f = open("misspelled_names", "a")
				f.write(Actor['name'] + " : " + actor_name + ",\n")
				
				self.render("game_round.html", title='title', 
							movie=movie,players=players, game_id=game_id)
			else:

				enter_actor_in_actors_db(Actor)

				movie = return_appropriate_movie(actor_or_actress(Actor))
				
				enter_movie_in_actors_db(movie, Actor.personID)
				push_ratings_scores_in_game_db(game_id, movie['critics_score'], movie['audience_score'])
				movie_list = actor_or_actress(Actor)
				tornado.ioloop.IOLoop.instance().call_later(1, enter_all_movies_in_both_dbases, 
															movie_list, Actor.personID,
															 game_id)

				self.render("game_round.html", title='title', 
							movie=movie,players=players, game_id=game_id)
		else:

			movie_list = actor_db_entry
			movie = movie_list.pop(random.randint(0, len(movie_list) - 1))
			push_movies_from_actorDB_to_gameSessionsDB(game_id, movie_list, movie)
			
			self.render("game_round.html", title='title', 
						movie=movie,players=players, game_id=game_id)



	def post(self):
		pass


class ScoreHandler(tornado.web.RequestHandler):
	def get(self):
		print "We are in ScoreHandler"
		try:
			game_id = self.get_argument("game_id")
		except:
			self.redirect("/")
		print game_id
		game_entry = db.game_sessions.find({"_id": ObjectId(game_id)})

		players_guesses = {}
		players_penalties = {}
		critics_score = game_entry[0]['Critics']
		players_scores = game_entry[0]["Player scores"]

		for player in players_scores:
			player_guess = int(self.get_argument(player))
			players_guesses[player] = player_guess
			player_penalties = abs(critics_score - player_guess)
			players_scores[player] += player_penalties
			players_penalties[player] = player_penalties
		


		print db.game_sessions.update({"_id": ObjectId(game_id)}, 
									{"$set": {"Player scores": players_scores}})
		
		self.render("score_update.html", players_scores=players_scores,
										 players_guesses= players_guesses,
										 players_penalties=players_penalties,
										 critics_score=critics_score,
										 game_id=game_id)


class RoundHandler(tornado.web.RequestHandler):
	def get(self):
		print "We are in RoundHandler"
		
		try:
			game_id = self.get_argument("game_id")
			print game_id
		except:
			self.redirect("/")
		print game_id

		game_entry = db.game_sessions.find({"_id": ObjectId(game_id)})[0]

		# print game_entry

		players = []
		for player in game_entry["Player scores"]:
			players.append(player)

		movie = pick_movie_from_game_sessions_db(game_entry["Movies"], game_id)
		print "We have come this far."

		if not movie:
			self.render("nomovie.html")
			return False
		print db.game_sessions.update({"_id": ObjectId(game_id)}, 
										{ "$set":  {"Critics": movie['critics_score']}})
		print movie['title']
		self.render("game_round.html", movie=movie, players=players, game_id=game_id)


def pick_movie_from_game_sessions_db(movie_list, game_id):
	if len(movie_list) == 0:
		return False
	movie = movie_list.pop(random.randint(0, len(movie_list) - 1))
	db.game_sessions.update({"_id": ObjectId(game_id)},{"$set": {"Movies": movie_list}})
	return movie
	

def get_actor_object_from_imdb(actor_name):
	actor_object = imd.search_person(actor_name)[0]
	imd.update(actor_object)
	
	return actor_object


def start_game_session(players):
	player_guesses = {}
	for player in players:
		player_guesses[player] = 0
	game_id = db.game_sessions.insert({
										"Player scores": players,
										"Movies": [],
										# "Player guesses": player_guesses 
										})

	return game_id


def push_ratings_scores_in_game_db(game_id, critics_score, audience_score):

	db.game_sessions.update({"_id": game_id}, { "$set":  {"Critics": critics_score,
												"Audience": audience_score} 
												})


def push_movies_from_actorDB_to_gameSessionsDB(game_id, movie_list, movie):
	db.game_sessions.update({"_id": ObjectId(game_id)}, 
							{"$set": {"Movies": movie_list,
							 "Critics": movie['critics_score']}})


def create_player_dict(players_str):
	players_list = players_str.split(',')
	players = {}
	for player in players_list:
		players[player.strip()] = 0

	return players


def is_actor_in_actors_db(actor_name):
	actor_PersonID = False
	split_name = actor_name.split(' ')
	#remove count from number_actors_in_db
	actor_entry_in_db = db.actors.find({ "$and": [{'Last Name': split_name [-1].strip()},
													{'First Name': split_name[0].strip()} ] }) 
	print actor_entry_in_db	
 	
 	if actor_entry_in_db.count() > 0:
 		return actor_entry_in_db[0]["Movies"]
 	else:
 		# return False, False
 		return False



def enter_game_session_info_in_game_db(critics_score, audience_score, players):
	player_guesses = {}
	for player in players:
		player_guesses[player] = 0

	game_id = db.game_sessions.insert({"Player scores": players, 
										"Critics": critics_score, 
										"Audience": audience_score, 
										"Player guesses": player_guesses,
										"Movies": []
										})

	return game_id



def actor_or_actress(actor):
	print "We are in actor_or_actress."
	if 'actor' in actor.keys():
		return actor['actor']
	else:
		return actor['actress']


def pick_random_movie_object(movie_list):
	return movie_list.pop(random.randint(0, len(movie_list) - 1))


def return_appropriate_movie(movie_list):
	print "We are in return_appropriate_movie"

	useful = False
	while not useful and len(movie_list) > 0:
		movie = pick_random_movie_object(movie_list)

		if not movie_has_relevant_keys(movie):
			continue
		has_reviews = check_for_rt_reviews(movie.movieID)
		if not has_reviews:
			continue
		critics_score, audience_score, rt_id = has_reviews
		if not has_more_than_five_reviews(rt_id):
			continue
		useful = True
	
	if not useful:
		return False
	print "We are returning a movie."
	print movie
	return prepare_movie_dict_entry(movie, critics_score, audience_score)


def movie_has_relevant_keys(movie):
	print "We are in movie_has_relevant_keys"
	if "year" not in movie.keys():
		return False
	update_movie_info(movie)
	print movie.keys()
	if not all(key in movie.keys() for key in ("director", "plot outline", "plot",
												 "cast", "full-size cover url")):
		print "Not all keys"
		return False
	else:
		print "Has all keys()"
		return True


def check_for_rt_reviews(movieID):
	"""remove movies that have no reviews"""
	print "We are in check_for_rt_reviews"
	result = request_rt_ratings(movieID)
	print result
	if not result:
		return False
	critics, audience, rt_movie_id = result
	if critics < 0 or not critics or not audience:
		return False
	elif not has_more_than_five_reviews(rt_movie_id):
		return False
	else:
		return critics, audience, rt_movie_id

def request_json_from_rt(movieID, request_type):
	"""send a json request to RT.com for the movie's ratings scores"""
	print "What is the request type? in request_json_from_rt"
	print request_type

	key= os.environ['rt_key']
	if request_type == "movie_alias":
		print "movie_alias"
		url_string = "http://api.rottentomatoes.com/api/public/v1.0/" + request_type + ".json?apikey=" + key + "&type=imdb&id=" + movieID
		print url_string
	elif request_type == "reviews":
		print "reviews"
		url_string = "http://api.rottentomatoes.com/api/public/v1.0/movies/" + movieID +"/reviews.json?apikey=" + key
		print url_string
	else:
		print "something went wrong with request_json_from_rt"


	return json.load(urllib2.urlopen(url_string))


def request_rt_ratings(movieID):
	"""send a json request to RT.com for the movie's ratings scores"""
	json_data = request_json_from_rt(movieID, "movie_alias")
	
	return parse_json_for_scores(json_data)


def parse_json_for_scores(json_data):
	"""parse json from RT.com's response if it has ratings scores"""
	if 'ratings' in json_data:
		critics_score = json_data['ratings']['critics_score']
		audience_score = json_data['ratings']['audience_score']
		rt_movie_id = json_data['id']

		return critics_score, audience_score, rt_movie_id
	else:
		return False


def has_more_than_five_reviews(movie_id):
	total_reviews = request_number_of_rt_reviews(movie_id)
	if total_reviews < 6:
		return False
	else:
		return True

def request_number_of_rt_reviews(imdb_id):
	json_data = request_json_from_rt(str(imdb_id), "reviews")
	print "Printing JSON Data"
	print json_data

	print parse_json_for_total_reviews_number(json_data)
	return parse_json_for_total_reviews_number(json_data)

def parse_json_for_total_reviews_number(json_data):
	return json_data['total']


def enter_actor_in_actors_db(actor):
	
	split_name = actor['canonical name'].split(",")

	db.actors.insert({
					"IMDb PersonID": actor.personID, 
					"Last Name": split_name[0].strip(),
					"First Name": split_name[1].strip(),
					# "Birth year": actor['birth date'],
					# "Biography": actor['bio'],
					"Movies": []

					})

def enter_movie_in_actors_db(movie, actor_id):

	db.actors.update({"IMDb PersonID": actor_id}, { "$push": {"Movies": movie }})

	print "Entered one movie of this actor/actress."


def enter_all_movies_in_both_dbases(movie_list, actor_id, game_id):
	print "In enter_all_movies_in_both_dbases"
	if len(movie_list) > 0:
		movie = return_appropriate_movie(movie_list)
		if not movie:
			return
		enter_movie_in_actors_db(movie, actor_id)
		enter_movie_into_game_db(movie, game_id)
		print "Entered one movie in both dbases."
		tornado.ioloop.IOLoop.instance().call_later(1, enter_all_movies_in_both_dbases, 
													movie_list, actor_id,
										 			game_id)
	else:
		print "Finished enter_all_movies_in_both_dbases"



def enter_movie_into_game_db(movie, game_id):
	db.game_sessions.update({"_id": ObjectId(game_id)}, {"$push": {"Movies": movie}})


def prepare_movie_dict_entry(movie, critics_score, audience_score):
	movie_dict = {'title': movie['title'], 
					'year': movie['year'],
		 			'director': movie['director'][0]['name'],
		 			'plot outline': movie['plot outline'],
		 			'plot': movie['plot'][0],
		 			'full-size cover url': movie['full-size cover url'],
		 			"critics_score": critics_score,
		 			"audience_score": audience_score  
		 			}


	cast = []
	for i in range(len(movie['cast'])):
		cast.append(movie['cast'][i]['name'])
	movie_dict['cast'] = cast


	return movie_dict


def update_movie_info(movie):
	print "updating movie"
	return imd.update(movie)


application = tornado.web.Application([
										(r"/", MainHandler),
										(r"/game", GameHandler),
										(r"/score_update", ScoreHandler),
										(r"/next_round", RoundHandler)
										],
										static_path="static",
										debug=True)

if __name__ == "__main__":
	application.listen(8888)
	tornado.autoreload.start()
	tornado.ioloop.IOLoop.instance().start()
