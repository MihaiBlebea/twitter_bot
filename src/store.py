import sqlite3

conn = sqlite3.connect("store.db")

TABLE_NAME = "schedules"

class Schedule():
	def __init__(self, post, link, twitter_username, created = None):
		self.id = None
		self.post = post
		self.link = link
		self.twitter_username = twitter_username
		self.created = created


def insert(schedule: Schedule) -> Schedule:
	cursor = conn.cursor()
	query = "INSERT INTO {} (post, link, twitter_username) VALUES (\"{}\", \"{}\", \"{}\")".format(
		TABLE_NAME,
		schedule.post,
		schedule.link,
		schedule.twitter_username
	)
	
	cursor.execute(query)

	conn.commit()

	schedule.id = cursor.lastrowid

	cursor.close()

	return schedule


def select_next_unposted() -> Schedule:
	cursor = conn.cursor()
	row = cursor.execute(f"""SELECT * FROM {TABLE_NAME} WHERE id NOT IN (
		SELECT post_id FROM posted
	) ORDER BY id ASC""").fetchone()

	if row == None:
		return None
		
	return from_row_to_model(row)


def mark_as_posted(id : int) -> None:
	table = "posted"
	cursor = conn.cursor()
	query = "INSERT INTO {} (post_id) VALUES (\"{}\")".format(
		table,
		id
	)
	
	cursor.execute(query)
	conn.commit()
	cursor.close()


def get_posted_today() -> list:
	cursor = conn.cursor()
	rows = cursor.execute(f"""SELECT * FROM {TABLE_NAME} WHERE id IN (
		SELECT post_id FROM posted WHERE date(created) = date('now')  
	) ORDER BY id ASC""").fetchall()

	schedules = []
	for row in rows:
		schedules.append(from_row_to_model(row))
		
	return schedules


def from_row_to_model(row) -> Schedule:
	s = Schedule(row[1], row[2], row[3], row[4])
	s.id = row[0]

	return s