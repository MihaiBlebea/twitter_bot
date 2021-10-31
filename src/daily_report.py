from dotenv import dotenv_values

from store import get_posted_today, get_today_followers
from telegram import send_message


def main():
	config = dotenv_values(".env")

	schedules = get_posted_today()
	followers_count = get_today_followers()

	message = f"Posted {len(schedules)} today on twitter and got +{ len(followers_count) } new followers."
	send_message(message, config["BOT_TOKEN"], config["CHAT_ID"])


if __name__ == "__main__":
	main()