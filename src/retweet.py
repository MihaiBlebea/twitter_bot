import tweepy
from dotenv import dotenv_values

from telegram import send_message


def main():
	config = dotenv_values(".env")

	print("starting...")
	auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
	auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

	api = tweepy.API(auth)
	tweets = api.search_tweets(q="#golang", lang="en", result_type="popular")
	tweet = tweets[0]

	tweet.retweet()

	message = f"RT: {tweet.text}"
	send_message(message, config["BOT_TOKEN"], config["CHAT_ID"])
	

if __name__ == "__main__":
	main()