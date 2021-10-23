import unittest
import sqlite3

from src.content import fetch_devto
from src.store import from_rows_to_posts, insert_post, select_next_unposted, mark_as_posted


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

	def test_can_fetch_content_from_devto(self):
		"""
        Test that can fetch content from devto and insert into database
        """
		posts = fetch_devto(1)
		for post in posts:
			insert_post(post, self.conn)

		validate_post = posts[0]

		total_posts = self.__all_posts()

		self.assertEqual(len(total_posts), 100, "this shoud be equal")
		self.assertEqual(total_posts[0].source_id, validate_post.source_id)
		self.assertEqual(total_posts[0].content, validate_post.content)
		self.assertEqual(total_posts[0].link, validate_post.link)
		self.assertEqual(total_posts[0].twitter_username, validate_post.twitter_username)


	def test_can_fetch_next_unposted_post(self):
		"""
        Test that after saving the content to database, we can fetch a post, mark it as posted
		and the next article requested should be the next unposted one
        """
		posts = fetch_devto(1)
		for post in posts:
			insert_post(post, self.conn)
		
		first_post = posts[0]
		second_post = posts[1]
		
		post = select_next_unposted(self.conn)

		self.assertEqual(post.source_id, first_post.source_id)

		mark_as_posted(post.id, self.conn)

		post = select_next_unposted(self.conn)

		self.assertEqual(post.source_id, second_post.source_id)


	def test_not_fetching_duplicate_content(self):
		"""
		Fetch 100 articles from devto, save them to the database.
		Fetch another 100 articles from devto, save them to the database.
		Test that the total amount of articles in the database is still 100.
		"""
		posts = fetch_devto(1)
		for post in posts:
			insert_post(post, self.conn)

		posts = fetch_devto(1)
		for post in posts:
			insert_post(post, self.conn)

		total_posts = self.__all_posts()

		self.assertEqual(len(total_posts), 100, "this shoud be equal")


	def __all_posts(self) -> int:
		cursor = self.conn.cursor()
		rows = cursor.execute("SELECT * FROM posts").fetchall()

		return from_rows_to_posts(rows)
