#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" #Changes directory to directory of this file
echo "$MINUTE $HOUR $DAY $MONTH $DAYOFWEEK cd $DIR && python logger.py" | crontab -                #Adds command to crontab
