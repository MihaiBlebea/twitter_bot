import tweepy
from dotenv import dotenv_values

from scheduler import get_next_post, mark_posted
from content import fetch_devto
from telegram import send_message
from store import Schedule, select_next_unposted, update_as_posted


def main():
	config = dotenv_values(".env")

	print("starting...")
	auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
	auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

	api = tweepy.API(auth)

	schedule = select_next_unposted()
	if schedule == None:
		# get some new posts
		print("no more posts, fetch some more")
		fetch_devto()

		schedule = select_next_unposted()

	# post = get_next_post()
	# if post == None:
	# 	print("no post found")
		
	# 	fetch_devto()
	# 	post = get_next_post()


	# trends = api.available_trends()
	# save_to_json(trends)
	
	# london_plance_id = 44418
	# trends = api.get_place_trends(london_plance_id)

	# trend = trends[0]["trends"][0]
	# tweets = api.search_tweets(q=trend["query"], lang="en")
	# # save_to_json(tweets, "tweets")
	# print(tweets.removeStatus)
	print(schedule)
	# res = api.update_status(post["post"])
	# print(res)

	send_message(schedule.post, config["BOT_TOKEN"], config["CHAT_ID"])

	update_as_posted(schedule.id)
	# mark_posted(schedule.link)


if __name__ == "__main__":
	main()