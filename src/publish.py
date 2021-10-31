import tweepy
from dotenv import dotenv_values

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
		print("no more content")
		send_message(
			"There is no more content. Please add more", 
			config["BOT_TOKEN"], 
			config["CHAT_ID"],
		)
		return
	
	api.update_status(post.content)

	send_message(post.content, config["BOT_TOKEN"], config["CHAT_ID"])

	mark_as_posted(post.id)


if __name__ == "__main__":
	main()