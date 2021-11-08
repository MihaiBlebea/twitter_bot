import tweepy
from dotenv import dotenv_values
import argparse

from telegram import send_message

class Retweet():

	def __init__(self):
		# create the config from env file
		self.config = dotenv_values(".env")

		# create the api client
		auth = tweepy.OAuthHandler(self.config["CONSUMER_KEY"], self.config["CONSUMER_SECRET"])
		auth.set_access_token(self.config["ACCESS_TOKEN"], self.config["ACCESS_TOKEN_SECRET"])

		self.api = tweepy.API(auth)

	def retweet(self, tag: str):
		tweets = self.api.search_tweets(q=tag, lang="en", result_type="popular")

		# check if the tweets are older then the last published one

		# pick one tweet which meets the criteria
		tweet = tweets[0]

		# retweet it
		tweet.retweet()

		# save the retweet to the db

		# send update to telegram
		message = f"RT: {tweet.text}"
		send_message(message, self.config["BOT_TOKEN"], self.config["CHAT_ID"])


def main():
	parser = argparse.ArgumentParser(
		prog= "twitter_bot", 
		usage="%(prog)s [options]", 
		description="post retweet on twitter.",
	)

	parser.add_argument(
		"-q",
		dest="query",
		required=True, 
		help="query for the tag to search latest tweets",
	)

	args = parser.parse_args()

	retweeter = Retweet()
	retweeter.retweet(args.query)
	

if __name__ == "__main__":
	main()