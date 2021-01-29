#!/usr/bin/env python3
import subprocess

#uses bash to excecute
class Start:
        subprocess.check_call(['bash', 'src/cronjob.sh'])