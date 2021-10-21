import requests
import json 
from store import Schedule, insert, check_if_url_exists

CHARACTER_LIMIT = 280

def main():
	fetch_devto(True)


def fetch_devto(save_file : bool = False) -> None:
	"""
	Fetches content from dev.to website and saves it in the schedules csv file
	"""
	for page in range(16):
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
			posted = False
			tags = content["tag_list"]

			if check_if_url_exists(url) == False:
				post = prepare_post(
					raw_content, 
					author,
					url,
					tags
				)

				insert(Schedule(post, url, author, posted))
			else:
				print("post already saved")


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
