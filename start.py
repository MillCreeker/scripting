#!/usr/bin/env python3
import subprocess
import src.Config as config

#uses bash to excecute
class Start:
        cronjob_minute = config.get_config("settings", "cronjob-minute")
        cronjob_hour = config.get_config("settings", "cronjob-hour")
        cronjob_day = config.get_config("settings", "cronjob-day")
        subprocess.call(['bash', 'cronjob.sh',cronjob_minute,cronjob_hour,cronjob_day])