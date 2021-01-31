#!/usr/bin/env python3
import datetime
import os

#uses creational pattern singelton to only use one instance at a time 
class Logger:
    __instance = None

    @staticmethod
    def get_instance():
        if Logger.__instance is None:
            Logger()
        return Logger.__instance

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self

    #used for successful backups
    def log(self, string):
        if not os.path.exists('log.txt'):
            f = open("log.txt", "w+")       #creates file if it doesn't exist
        f = open("log.txt", "a")
        f.write("\nSUCCESS\t " + str(datetime.datetime.now()) + ": " + string)
        f.close()

    #used for unsuccessful backups
    def err(self, string):
        if not os.path.exists('log.txt'):
            f = open("log.txt", "w+") #creates file if it doesn't exist
        f = open("log.txt", "a")
        f.write("\nERROR\t " + str(datetime.datetime.now()) + ": " + string)
        f.close()