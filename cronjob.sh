#!/usr/bin/env bash
#Changes directory to directory of this file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" 
#Adds command to crontab.
#$1 = minutes, $2 = hours, $3 = days
echo "$1 $2 $3 * * cd $DIR/src && python3 Main.py" | crontab -          
