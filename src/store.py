import sqlite3

conn = sqlite3.connect("store.db")

class Post():
	def __init__(self, source_id, content, link, twitter_username, created = None):
		self.id = None
		self.source_id = source_id
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


def insert_post(post: Post) -> Post:
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


def insert_follower(follower : Follower) -> Follower:
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


# def check_if_url_exists(url : str) -> bool:
# 	cursor = conn.cursor()
# 	row = cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE link = \"{url}\"").fetchone()

# 	if row == None:
# 		return False
		
# 	return True


def select_next_unposted() -> Post:
	cursor = conn.cursor()
	row = cursor.execute(f"""SELECT * FROM posts WHERE id NOT IN (
		SELECT post_id FROM posted
	) ORDER BY id ASC""").fetchone()

	if row == None:
		return None
		
	return from_row_to_post(row)


def mark_as_posted(id : int) -> None:
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

	posts = []
	for row in rows:
		posts.append(from_row_to_post(row))
		
	return posts


def from_row_to_post(row) -> Post:
	p = Post(row[1], row[2], row[3], row[4])
	p.id = row[0]

	return p