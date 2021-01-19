#!/usr/bin/env python3
import datetime
import os

#config = open(".config", "r")
#to_backup = config.readlines()


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
    f.write("\nERROR  \t "+str(datetime.datetime.now())+" " + string + ":");
    f.close();

log("success")
err("error")
