from crontab import CronTab
import getpass
import argparse

COMMAND = "cd ${HOME}/twitter_bot && ./publish.sh >> ${HOME}/twitter_bot_logs.log 2>&1"

def main():
	parser = argparse.ArgumentParser(
		prog= "crontab", 
		usage="%(prog)s [options]", 
		description="install or uninstall the cron commands.",
	)

	parser.add_argument(
		"-u",
		dest="uninstall",
		action="store_true", 
		required=False, 
		help="uninstall?",
	)

	parser.add_argument(
		"-i",
		dest="install",
		action="store_true", 
		required=False, 
		help="install?",
	)

	args = parser.parse_args()

	user = getpass.getuser()
	cron = CronTab(user=user)

	if args.uninstall == True:
		print("uninstall...")
		uninstall(cron)
		return

	if args.install == True:
		print("install...")
		install(cron)
		return


def install(cron):
	# check if the command already exists
	if exists(cron, COMMAND):
		print("command already exists")
		return

	# install this command as a cron
	job = cron.new(
		command=COMMAND, 
		comment="this command will run the posting script for twitter_bot",
	)
	job.minute.every(1)
	cron.write()


def uninstall(cron):
	iter = cron.find_command(COMMAND)
	for job in iter:
		cron.remove(job)

	cron.write()


def exists(cron, command):
	iter = cron.find_command(command)
	if len(list(iter)) > 0:
		return True
	
	return False
	

if __name__ == "__main__":
	main()