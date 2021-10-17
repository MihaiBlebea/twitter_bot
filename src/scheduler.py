import csv

SCHEDULER_FILE = "scheduler.csv"

def schedule(contents : list) -> None:
	"""
	schedule accepts a list of contents, 
	loops over them and saves each as a new line in the csv file.
	"""
	with open(SCHEDULER_FILE, mode="w") as file:
		headers = ["post", "url", "twitter_author", "posted"]
		w = csv.DictWriter(file, fieldnames=headers)

		w.writeheader()
		for content in contents:
			w.writerow({
				"post": content[0], 
				"url": content[1],
				"twitter_author": content[2], 
				"posted": content[3],
			})


def get_next_post() -> dict:
	"""
	get next post where posted is False
	"""
	with open(SCHEDULER_FILE, mode="r") as file:
		r = csv.DictReader(file)
		for row in r:
			if row["posted"] == "False":
				return row

	return None


def mark_posted(url : str) -> None:
	"""
	find the post by url and update it marking as posted, then save the records as csv
	"""
	op = open(SCHEDULER_FILE, "r")
	r = csv.DictReader(op)
	
	rows = []
	for row in r:
		# find row by url and mark as posted
		if row["url"] == url:
			row["posted"] = True
			
		rows.append([
			row["post"], 
			row["url"], 
			row["twitter_author"], 
			row["posted"],
		])

	schedule(rows)