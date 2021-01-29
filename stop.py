#!/usr/bin/env python3
import subprocess

# only works on windows for now
class Stop:
        subprocess.check_call(['wsl', 'crontab', '-r'])