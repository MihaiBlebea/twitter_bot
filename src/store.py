#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect("store.db")

TABLE_NAME = "schedules"

class Schedule():
	def __init__(self, post, link, twitter_username, posted):
		self.id = None
		self.post = post
		self.link = link
		self.twitter_username = twitter_username
		self.posted = posted


def insert(schedule: Schedule) -> Schedule:
	cursor = conn.cursor()
	cursor.execute(
		"INSERT INTO {} (post, link, twitter_username, posted) VALUES ('{}', '{}', '{}', '{}')".format(
			TABLE_NAME,
			schedule.post,
			schedule.link,
			schedule.twitter_username,
			schedule.posted
		)
	)

	conn.commit()

	schedule.id = cursor.lastrowid

	cursor.close()

	return schedule


def select_all() -> list:
	cursor = conn.cursor()
	rows = cursor.execute(f"SELECT * FROM {TABLE_NAME}").fetchall()

	schedules = []
	for row in rows:
		s = from_row_to_model(row)
		schedules.append(s)

	return schedules


def from_row_to_model(row) -> Schedule:
	s = Schedule(row[1], row[2], row[3], row[4])
	s.id = row[0]

	return s
