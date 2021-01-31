#!/usr/bin/env python3
import subprocess

# is called via wsl and only works on windows for now
# stops cronjob via crontab -r which removes all current cronjobs
class Stop:
        subprocess.call(['wsl', 'crontab','-r'])