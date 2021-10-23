import sqlite3

conn = sqlite3.connect("store.db")


class Post():
	def __init__(self, source_id, content, link, twitter_username, created = None):
		self.id = None
		self.source_id = str(source_id)
		self.content = content
		self.link = link
		self.twitter_username = twitter_username
		self.created = created


class Follower():
	def __init__(self, twitter_id, real_name, screen_name, image_url, created = None):
		self.id = None
		self.twitter_id = twitter_id
		self.real_name = real_name
		self.screen_name = screen_name
		self.image_url = image_url
		self.created = created


def insert_post(post: Post, conn=conn) -> Post:
	cursor = conn.cursor()
	query = """INSERT OR IGNORE INTO posts (source_id, content, link, twitter_username) 
	VALUES (\"{}\", \"{}\", \"{}\", \"{}\")""".format(
		post.source_id,
		post.content,
		post.link,
		post.twitter_username
	)
	
	cursor.execute(query)

	conn.commit()

	post.id = cursor.lastrowid

	cursor.close()

	return post


def insert_follower(follower : Follower, conn=conn) -> Follower:
	cursor = conn.cursor()
	query = """INSERT OR IGNORE INTO followers 
	(twitter_id, real_name, screen_name, image_url) 
	VALUES (\"{}\", \"{}\", \"{}\", \"{}\")""".format(
		follower.twitter_id,
		follower.real_name,
		follower.screen_name,
		follower.image_url,
	)
	
	cursor.execute(query)

	conn.commit()

	follower.id = cursor.lastrowid

	cursor.close()

	return follower


def select_next_unposted(conn=conn) -> Post:
	cursor = conn.cursor()
	row = cursor.execute(f"""SELECT * FROM posts WHERE id NOT IN (
		SELECT post_id FROM posted
	) ORDER BY id ASC""").fetchone()

	if row == None:
		return None
		
	return from_row_to_post(row)


def mark_as_posted(id : int, conn=conn) -> None:
	cursor = conn.cursor()
	query = f"INSERT INTO posted (post_id) VALUES (\"{id}\")"
	cursor.execute(query)
	conn.commit()
	cursor.close()


def get_posted_today() -> list:
	cursor = conn.cursor()
	rows = cursor.execute(f"""SELECT * FROM posts WHERE id IN (
		SELECT post_id FROM posted WHERE date(created) = date('now')  
	) ORDER BY id ASC""").fetchall()

	return from_rows_to_posts(rows)


def get_followers_count(conn=conn) -> int:
	cursor = conn.cursor()
	row = cursor.execute("SELECT count(id) FROM followers").fetchone()

	return row[0]


def from_row_to_post(row) -> Post:
	p = Post(row[1], row[2], row[3], row[4])
	
	if row[4] == "None":
		p.twitter_username = None
	p.id = row[0]

	return p


def from_rows_to_posts(rows : list) -> list:
	posts = []
	for row in rows:
		posts.append(from_row_to_post(row))
		
	return posts


def from_row_to_follower(row) -> Follower:
	f = Follower(row[1], row[2], row[3], row[4])
	
	f.id = row[0]

	return f


def from_rows_to_followers(rows : list) -> list:
	followers = []
	for row in rows:
		followers.append(from_row_to_follower(row))
		
	return followers