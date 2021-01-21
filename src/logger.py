#!/usr/bin/env python3
import datetime
import os 

config = open(".config", "r")
to_backup = config.readlines()

class logger:
    class __logger:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if not logger.instance:
            logger.instance = logger.__logger(arg)
        else:
            logger.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)

    def log(string):
        if not os.path.exists('logger.txt'):
            f=open("logger.txt","w+");
        f=open("logger.txt","a");
        f.write("\nSUCCESS\t "+str(datetime.datetime.now())+" " + string + ":");
        f.close();

    def err(string):
        if not os.path.exists('logger.txt'):
            f=open("logger.txt","w+");
        f=open("logger.txt","a");
        f.write("\nERROR\t "+str(datetime.datetime.now())+" " + string + ":");
        f.close();

    log("success")
    err("error")
