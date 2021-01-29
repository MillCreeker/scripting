#!/usr/bin/env python3
import datetime
import os
import subprocess 
class logger:
    instance = None

    @staticmethod 
    def getInstance():
        if logger.instance == None:
            logger()
        return logger.instance
    def init(self):
        if logger.instance != None:
            raise Exception("This class is a singleton!")
        else:
            logger.__instance = self

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

var1="1"
var2="1"
var3="1"
var4="1"
var5="1"

subprocess.call("cronjob.sh && echo test",shell=True)
#subprocess.call('bash',1,"cronjob.sh", shell=True)
#subprocess.Popen(['cronjob.sh %s %s %s %s %s' % (var1, var2, var3, var4, var5)], shell = True)