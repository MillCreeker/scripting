#!/usr/bin/env python3
import datetime
import os
import subprocess


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

    def log(self, string):
        if not os.path.exists('logger.txt'):
            f = open("logger.txt", "w+")
        f = open("logger.txt", "a")
        f.write("\nSUCCESS\t " + str(datetime.datetime.now()) + ": " + string)
        f.close()

    def err(self, string):
        if not os.path.exists('logger.txt'):
            f = open("logger.txt", "w+")
        f = open("logger.txt", "a")
        f.write("\nERROR\t " + str(datetime.datetime.now()) + ": " + string)
        f.close()
