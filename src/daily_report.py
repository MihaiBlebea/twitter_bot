from dotenv import dotenv_values

from store import get_posted_today;
from telegram import send_message


def main():
	config = dotenv_values(".env")

	schedules = get_posted_today()
	
	message = f"Posted {len(schedules)} today on twitter today."
	send_message(message, config["BOT_TOKEN"], config["CHAT_ID"])

if __name__ == "__main__":
	main()