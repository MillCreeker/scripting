# Repository group 1

## About

This is collection of scripts that have the purpose of serving as a backusystem for important files that need regular backups. It can be used by anyone that has python and a bash command line be it native on linux or a windows subsytem (wsl, Ubuntu etc.)

### Authors/Contributors

* [Tobias Weigl](mailto:tobias.weigl@edu.fh-joanneum.at)
* [Jan Mühlbacher](mailto:jan.muehlbacher@edu.fh-joanneum.at)
* [Sebastian Toporsch](mailto:sebastian.toporsch@edu.fh-joanneum.at)

## BackUpr

### Description

Backupsytem to Database. The system has a ".config" File that determines the files that are saved. The backup is done in set intervals. The files are then saved on a database named backUpr, that gets called by the script.

The script checks if the selected file is saved correctly on the database.

The result of the backup is documented in a log file named log.txt.

In the log.txt successful backups start with SUCCESS and errors start with ERROR followed by the time and a success message/error message.

### Criteria used in the project:

* Access to Files
* Access to Database
* Regex
* Runnable as cronjob

# Starting the project

* start your cron if it is not already running by running "sudo service cron start"
* run "python start.py"

# Stopping the Project

* run "sudo service cron stop" followed by:
  * Windows: "python stop.py" to remove cronjob
  * Linux: "crontab -r" to remove cronjob
