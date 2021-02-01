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

# Installation/Prerequisites for this project
1. Python/Python3
2. A running MySQL Database
3. Linux subsystem with python installed (Only for Windows users)
4. Start cron if it’s not already running. 
5. Do this by executing the following command: “sudo service cron start”


# Run/Execute
In order to execute the back-up script you just have to run the ‘start.py’ script. 
It will automatically read your configurations from the .config file and run at the desired frequency, backing up/deleting back-ups as you configured it.

If the script shall not run anymore, and thus generate no new back-ups, you can stop it by executing the ‘stop.py’ script. 
The ‘stop.py’ script will only work on Windows with a Linux subsystem, because it uses wsl to execute ‘crontab -r’. Linux-Users will have to stop the crontab manually.


# Custom configuration
## File configurations 
Many parameters can be adjusted to the user’s desires. This is accomplished through the use of a .config file. Within it one can specify certain tags which will influence certain parameters.
The general structure to specify which files shall be included in a given back-up looks like this:
```
“[tag-name]”: {
	[parameter 1]
	[parameter 2]
}
```

The tags which can be used are:

### include:
Every file within this tag will be included in the back-up.

### match:
Every file which includes a specified string within this tag will be included in the back-up. 
For example a parameter ‘.txt’ would include every text-file without having to specify every such file within the ‘include’-tag.

### exclude (optional):
Every file specified within this tag will not be included in the back-up. This tag may be used in connection with the ‘match’-tag in order to include every ‘.txt’ file except for the ‘not_include.txt’ file for example.
Note that at least a ‘include’- or ‘match’-tag needs to be present and that the files - which are ought to be backed-up - need to be within the ‘files’ folder!

## Other configurations
Every other kind of tag serves the adjustment of a certain specification for the back-up. These follow this general structure:
```
“[tag-name]”: {
	“[variable 1]”: “[value 1]”
	“[variable 2]”: “[value 2]”
```
The tags and variables within are:

### settings:
Used to specify the back-up frequency and time for deletion of backed-up files. 
Anything beneath the min and beyond the max value will not work therefore not executing the script, because the cronjob will throw an error.

##### cronjob-minute (optional):
Specifies at which minute of an hour the script shall be executed.
The min value is 1 and the max value is 59.

##### cronjob-hour (optional):
Specifies at which hour of the day the script shall be executed.
The min value is 1 and the max value is 23.

##### cronjob-day (optional):
Specifies at which day of the month the script shall be executed.
The min value is 1 and the max value is 30/31.

##### backup-frequency:
Specifies how often the script shall be executed. 0 means just once now, 1 means every day, 2 means every other day, etc.

##### delete-after (optional):
Specifies after how many days backed-up files shall be marked as deleted on the database.

##### permanent-delete (optional):
Specifies after how many days the backed-up files shall be permanently deleted from the database.

### database-settings:
Configurations to establish a connection with the desired database to store the backed-up files in.

##### host:
Name of the host.

##### user:
Name of the user.

##### password:
Password for the database. If empty, write:
```“password”: “”```

##### database:
Name of the database which shall be used.

# Documentation
## Root-directory

### start.py
Executed by the user. Starts the back-up process. Calls the ‘cronjob.sh’ file and initiates the cronjob with given parameters from .config file.

### stop.py
Executed by the user. Stops the back-up process by executing the command ‘crontab -r’ therefore removing the cronjob. Only works on Windows!

### .config
Contains the back-up specifications of the user.

### cronjob.sh
Executes the ‘Main.py’ script at the specified times. Called by the ‘start.py’ script via cronjob.

### log.txt
Lists all log-entries from the ‘Logger.py’ script. 
Writes SUCCESS if file was backed-up correctly and without errors and writes ERROR if task executed with an error.

## src-directory
### \_\_init\_\_.py
Marks the directory as a module.

### Config.py
Extracts the information written in the ‘.config’ file (e.g. files which require a back-up, settings, etc.).

### DBConnection.py
Establishes a database connection when instantiated with the needed credentials. 
Includes a plethora of methods used for all kinds of interactions with the database. Main uses include but are not limited to:
 * establishing a connection to the database
 * uploading back-ups with a number of files to the database
 * deleting back-ups and files on the database

### Logger.py
A script used to log messages and exceptions in the log.txt file. Has methods log() and err() to log SUCCESS and ERROR messages.

### Main.py
Executes the main part of the back-up. Called by the ‘cronjob.sh’ script.

## files-directory
Files within this directory are subject to a back-up.

# Known Issues
We are aware that some features are currently not implemented perfectly due to the time constraint.

These include:
 * the inability to use most symbols (e.g. ‘*’, ‘#’, ‘+’, etc) in the ‘.config’ file
 * the inconsistent way the cronjob works - it does not always work on every operating system
 * cronjob.sh can not take ‘*’ as an input parameter therefore eliminating the possibility of executing a cronjob every minute or hour for example. 
 * Cronjob was implemented so that the user has to input minutes, hours and days. Therefore, the back-up is intended to be executed on a certain day, hour and minute of a month.
 * ‘stop.py’ only works on Windows with wsl
