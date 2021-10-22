import unittest
from store import insert


class TestStore(unittest.TestCase):

	def test_insert_schedule(self):
		self.assertEqual(1, 2, "this shoud be equal")

if __name__ == "__main__":
	unittest.main()