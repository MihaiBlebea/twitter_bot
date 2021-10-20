import requests
import json
# from scheduler import 
from store import Schedule, insert

CHARACTER_LIMIT = 280

def main():
	fetch_devto()


def fetch_devto(save_to_json : bool = False) -> None:
	"""
	Fetches content from dev.to website and saves it in the schedules csv file
	"""
	tags = ["elixir", "go", "golang", "functional", "python"]
	divider = ","
	page = 1
	url = f"https://dev.to/api/articles?tags={divider.join(tags)}&per_page=100&page={page}"
	r = requests.get(url)

	if r.status_code >= 300:
		return None

	contents = r.json()

	if save_to_json == True:
		save_to_json(contents, "contents")

	for content in contents:
		raw_content = content["title"] + " " + content["description"]
		url = content["url"]
		author = content["user"]["twitter_username"]
		posted = False
		tags = content["tag_list"]

		post = prepare_post(
			raw_content, 
			author,
			url,
			tags
		)

		insert(Schedule(post, url, author, posted))


def prepare_post(content : str, author : str, url : str, tags : list = []) -> str:
	# removes excesive whitespaces
	content = content.replace("  ", " ").replace("\"", "")

	content_length = CHARACTER_LIMIT - len(url) - 2 #space characters
	if author is not None:
		content_length = content_length - len(author) - 3

	if len(tags) > 0:
		tags_length = 0
		for t in tags:
			tags_length += len(t) + 2

		content_length = content_length - tags_length

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
