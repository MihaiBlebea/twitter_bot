import requests
import json 
from dotenv import dotenv_values

from store import Post, insert_post

CHARACTER_LIMIT = 280

config = dotenv_values(".env")

def main():
	posts = fetch_devto(1)
	for post in posts:
		insert_post(post)


def fetch_devto(max_pages : int) -> None:
	"""
	Fetches content from dev.to website and saves it in the schedules csv file
	"""
	posts = []
	for page in range(max_pages):
		url = f"https://dev.to/api/articles?tag=go&tags_exclude=react&state=raising&per_page=100&page={page + 1}"
		r = requests.get(url)

		if r.status_code >= 300:
			return None

		contents = r.json()

		for content in contents:
			raw_content = content["title"]
			url = content["url"]
			author = content["user"]["twitter_username"]
			twitter_id = content["id"]
			tags = content["tag_list"]

			if check_is_english(raw_content) is False:
				continue

			post = prepare_post(
				raw_content, 
				author,
				url,
				tags
			)

			posts.append(Post(twitter_id, post, url, author))

	return posts


def prepare_post(content : str, author : str, url : str, tags : list = []) -> str:
	# removes excesive whitespaces
	content = content.replace("  ", " ").replace("\"", "")

	if author is not None:
		content += f" @{author}"

	if len(tags) > 0:
		content += f" {process_tags(tags)}"

	content += f" {url}"

	return content


def process_tags(tags : list) -> str:
	real_tags = []
	for t in tags:
		real_tags.append(f"#{t}")

	delimiter = " "

	return delimiter.join(real_tags)


def check_is_english(text: str) -> bool:
	url = "https://text-analysis12.p.rapidapi.com/language-detection/api/v1.1"

	payload = {
		"text": text
	}

	headers = {
		"content-type": "application/json",
		"x-rapidapi-host": "text-analysis12.p.rapidapi.com",
		"x-rapidapi-key": config["RAPID_API_KEY"]
	}

	r = requests.post(url, data=json.dumps(payload), headers=headers)

	if r.status_code != 200:
		return True

	body = r.json()

	if body["ok"] is False:
		return True

	if "en" not in body["language_probability"]:
		return False

	if float(body["language_probability"]["en"]) > 0.5:
		return True

	return False


if __name__ == "__main__":
	main()
