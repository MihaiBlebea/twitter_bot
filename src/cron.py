from crontab import CronTab
import getpass
import argparse

PUBLISH_CMD = "cd ${HOME}/twitter_bot && ./publish.sh >> ${HOME}/twitter_bot_logs.log 2>&1"
DAILY_REPORT_CMD = "cd ${HOME}/twitter_bot && ./daily_report.sh >> ${HOME}/twitter_bot_logs.log 2>&1"

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
		uninstall(cron, PUBLISH_CMD)
		uninstall(cron, DAILY_REPORT_CMD)
		return

	if args.install == True:
		print("install...")
		install(cron, PUBLISH_CMD, "5 8,11,12,15,17,19 * * *")
		install(cron, DAILY_REPORT_CMD, "0 21 * * *")
		return


def install(cron, cmd : str, schedule : str = "* * * * *") -> None:
	# check if the command already exists
	if exists(cron, cmd):
		print("command already exists")
		return

	# install this command as a cron
	job = cron.new(
		command=cmd, 
		comment="this command will run the posting script for twitter_bot",
	)
	job.setall(schedule)

	cron.write()


def uninstall(cron, cmd : str) -> None:
	iter = cron.find_command(cmd)
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