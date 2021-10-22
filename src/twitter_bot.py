import tweepy
from dotenv import dotenv_values

from content import fetch_devto
from telegram import send_message
from store import select_next_unposted, mark_as_posted


def main():
	config = dotenv_values(".env")

	print("starting...")
	auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
	auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

	api = tweepy.API(auth)
	
	post = select_next_unposted()
	if post == None:
		# get some new posts
		print("no more posts, fetch some more")
		fetch_devto()

		post = select_next_unposted()
	
	api.update_status(post.content)

	send_message(post.content, config["BOT_TOKEN"], config["CHAT_ID"])

	mark_as_posted(post.id)


if __name__ == "__main__":
	main()