import requests

def send_message(message : str, bot_token : str, chat_id : str) -> dict:
	url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}"
	response = requests.get(url)

	return response.json()


def send_photo(image_path : str, bot_token : str, chat_id : str, image_caption="") -> dict:
    data = {"chat_id": chat_id, "caption": image_caption}
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    with open(image_path, "rb") as image_file:
        ret = requests.post(url, data=data, files={"photo": image_file})
		
    return ret.json()