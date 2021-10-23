import tweepy
from dotenv import dotenv_values

from store import Follower, insert_follower


def main():
	followers = fetch_followers()
	for f in followers:
		insert_follower(f)


def fetch_followers() -> list:
	config = dotenv_values(".env")

	auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
	auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

	api = tweepy.API(auth)
	
	followers = api.get_followers()

	result = []
	for f in followers:
		follower = Follower(f.id, f.name, f.screen_name, f.profile_image_url_https)
		result.append(follower)

	return result


if __name__ == "__main__":
	main()