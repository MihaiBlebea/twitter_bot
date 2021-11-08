import tweepy
from dotenv import dotenv_values
import sqlite3
import argparse

from telegram import send_message


class Publisher():
	
	store_file = "store.db"

	character_limit = 280

	def __init__(self):
		# create the config from env file
		self.config = dotenv_values(".env")

		# create the db table
		self.conn = sqlite3.connect(self.store_file)
		self.cursor = self.conn.cursor()

		query = """CREATE TABLE IF NOT EXISTS posted (
			id INTEGER PRIMARY KEY,
			message TEXT,
			created DATETIME DEFAULT CURRENT_TIMESTAMP
		);"""
	
		self.cursor.execute(query)
		self.conn.commit()

		# create the api client
		auth = tweepy.OAuthHandler(self.config["CONSUMER_KEY"], self.config["CONSUMER_SECRET"])
		auth.set_access_token(self.config["ACCESS_TOKEN"], self.config["ACCESS_TOKEN_SECRET"])

		self.api = tweepy.API(auth)

	def publish(self, message: str, url: str = None, force: bool = False):
		if url is not None:
			message = f"{message}\n{url}"

		if force == False and self.__check_if_posted(message):
			print("this update was already posted")
			return

		self.api.update_status(message)
		send_message(message, self.config["BOT_TOKEN"], self.config["CHAT_ID"])

		self.__mark_posted(message)


	def __mark_posted(self, message: str):
		query = f"INSERT INTO posted (message) VALUES (\"{message}\")"
		self.cursor.execute(query)
		self.conn.commit()

	def __check_if_posted(self, message: str) -> bool:
		row = self.cursor.execute(f"SELECT id FROM posted WHERE message = \"{message}\"").fetchmany()

		if len(row) == 0:
			return False

		return True

def main():
	parser = argparse.ArgumentParser(
		prog= "twitter_bot", 
		usage="%(prog)s [options]", 
		description="post update on twitter.",
	)

	parser.add_argument(
		"-m",
		dest="message",
		required=True, 
		help="message to post",
	)

	parser.add_argument(
		"-u",
		dest="url",
		required=False, 
		default=None,
		help="url to post",
	)

	parser.add_argument(
		"-f",
		dest="force",
		required=False, 
		default=False,
		help="force to post the same url without checking",
	)

	args = parser.parse_args()

	print(args.message, args.url, args.force)
	publisher = Publisher()
	publisher.publish(args.message, args.url, args.force)


if __name__ == "__main__":
	main()