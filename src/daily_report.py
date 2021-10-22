from dotenv import dotenv_values
import tweepy

from store import get_posted_today;
from telegram import send_message


def main():
	config = dotenv_values(".env")

	schedules = get_posted_today()

	auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
	auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

	api = tweepy.API(auth)

	message = f"Posted {len(schedules)} today on twitter today."
	send_message(message, config["BOT_TOKEN"], config["CHAT_ID"])


if __name__ == "__main__":
	main()