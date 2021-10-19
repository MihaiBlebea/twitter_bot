import requests
import json
# from scheduler import 
from store import Schedule, insert

CHARACTER_LIMIT = 280

def main():
	fetch_devto()


def fetch_devto() -> None:
	"""
	Fetches content from dev.to website and saves it in the schedules csv file
	"""
	url = "https://dev.to/api/articles"
	r = requests.get(url)

	if r.status_code >= 300:
		return None

	contents = r.json()
	
	# save_to_json(contents, "contents")

	# schedules = []
	for content in contents:
		raw_content = content["title"] + " " + content["description"]
		url = content["url"]
		author = content["user"]["twitter_username"]
		posted = False

		post = prepare_post(
			raw_content, 
			author,
			url,
		)

		insert(Schedule(post, url, author, posted))

		# schedules.append([post, url, author, posted])

	# schedule(schedules)


def prepare_post(content : str, author : str, url : str) -> str:
	# removes excesive whitespaces
	content = content.replace("  ", " ")

	content_length = CHARACTER_LIMIT - len(url) - 2 #space characters
	if author is not None:
		content_length = content_length - len(author) - 3

	# if content length greater then allowed twitter length - url included, then add elipsis
	if len(content) > content_length:
		length_with_elipsis = content_length - 3
		content = content[:length_with_elipsis] + "..."

	if author is None:
		content = f"{content} {url}"
	else:
		content = f"{content} @{author} {url}"

	return content


def save_to_json(data, file_name : str) -> None:
	with open(f"{file_name}.json", "w") as outfile:
		json.dump(data, outfile)


if __name__ == "__main__":
	main()
