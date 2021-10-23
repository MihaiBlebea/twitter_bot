import unittest
import sqlite3

from src.followers import fetch_followers
from src.store import get_followers_count, insert_follower


class TestContent(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.conn = sqlite3.connect(":memory:")
		f = open("init.sql", "r")
		self.conn.cursor().executescript(f.read())
		self.conn.commit()

		f.close()

	@classmethod
	def tearDownClass(self):
		self.conn = None

	
	def test_can_fetch_followers(self):
		"""
		Fetch all followers from Twitter and save them to the database.
		Check the number of followers and the structure of the response.
		"""
		followers = fetch_followers()
		for f in followers:
			insert_follower(f, self.conn)

		validate_follower = followers[0]

		count = get_followers_count(self.conn)

		self.assertEqual(len(followers), count, "this shoud be equal")
		self.assertEqual(followers[0].twitter_id, validate_follower.twitter_id)
		self.assertEqual(followers[0].real_name, validate_follower.real_name)
		self.assertEqual(followers[0].screen_name, validate_follower.screen_name)
		self.assertEqual(followers[0].image_url, validate_follower.image_url)


	def test_not_fetching_duplicate_followers(self):
		"""
		Fetch all followers from Twitter and save them to the database.
		Fetch all followers again from Twitter and save them to the database.
		Validate that the number of followers in the database does not change.
		"""
		first_followers = fetch_followers()
		for f in first_followers:
			insert_follower(f, self.conn)

		second_followers = fetch_followers()
		for f in second_followers:
			insert_follower(f, self.conn)

		count = get_followers_count(self.conn)

		self.assertEqual(len(first_followers), count, "this shoud be equal")
