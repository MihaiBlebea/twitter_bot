import unittest
import sqlite3

from src.store import Post, Follower, get_posted_today, get_today_followers, insert_post, insert_follower, mark_as_posted


class TestContent(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.conn = sqlite3.connect(":memory:")
		f = open("init.sql", "r")
		self.conn.cursor().executescript(f.read())
		self.conn.commit()
		
		first_post = Post("1234", "content", "link", "username")
		second_post = Post("5678", "content", "link", "username")

		first_post = insert_post(first_post, self.conn)
		second_post = insert_post(second_post, self.conn)

		mark_as_posted(first_post.id)

		first_follower = Follower(1234, "real name", "screen_name", "image")
		second_follower = Follower(5678, "real name", "screen_name", "image")

		first_follower = insert_follower(first_follower, self.conn)
		second_follower = insert_follower(second_follower, self.conn)
		
		self.__update_follower_created_date_to_yesterday(self, first_follower.id)

		f.close()


	@classmethod
	def tearDownClass(self):
		self.conn = None

	
	def test_can_get_report_from_database(self):
		followers = get_today_followers()
		posts = get_posted_today()

		self.assertEqual(len(followers), 1, "this shoud be equal")
		self.assertEqual(len(posts), 1, "this shoud be equal")		


	def __update_follower_created_date_to_yesterday(self, id : int):
		cursor = self.conn.cursor()
		query = f"UPDATE followers SET created = DATE('now', '-1 day') WHERE id = '{id}'"

		cursor.execute(query)
		self.conn.commit()
		cursor.close()