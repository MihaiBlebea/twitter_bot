import requests
import json 
from src.store import Post, insert_post

CHARACTER_LIMIT = 280

def main():
	posts = fetch_devto(10, True)
	for post in posts:
		insert_post(post)


def fetch_devto(max_pages : int, save_file : bool = False) -> None:
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

		if save_file == True:
			save_to_json(contents, "contents")

		for content in contents:
			raw_content = content["title"]
			url = content["url"]
			author = content["user"]["twitter_username"]
			twitter_id = content["id"]
			tags = content["tag_list"]

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


def save_to_json(data, file_name : str) -> None:
	with open(f"{file_name}.json", "w") as outfile:
		json.dump(data, outfile)


if __name__ == "__main__":
	main()
