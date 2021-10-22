import tweepy
from dotenv import dotenv_values

from store import Follower, inser_follower


def main():
	config = dotenv_values(".env")

	print("starting...")
	auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
	auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

	api = tweepy.API(auth)
	
	followers = api.get_followers()
	for f in followers:
		inser_follower(Follower(f.id, f.name, f.screen_name, f.profile_image_url_https))


if __name__ == "__main__":
	main()