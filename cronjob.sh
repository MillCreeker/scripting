#!/usr/bin/env bash
#Changes directory to directory of this file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" 
#Adds command to crontab.
#$1 = minutes, $2 = hours, $3 = days, $4 = hours, $5 = hours
echo "$1 $2 $3 * * cd $DIR && python src/Main.py" | crontab -  
#echo "* * * * * cd $DIR && python3 src/Logger.py" | crontab -             
