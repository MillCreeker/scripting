#!/usr/bin/env python3

import re
from os import listdir
from os.path import isfile, join

# get configurations (for cronjob)
def get_config(setting_name, key_name):
    with open(".config", "r") as file:
        text = file.read()
    
    pattern = re.compile("\"" + setting_name + "\":\s*\{\s*([\n \"a-zA-Z0-9.:_-]*)\s*\}")
    settings = pattern.finditer(text)

    for e in settings:
        settings = e.group(1).replace("\t", "").replace(" ", "").split("\n")
    
    settings = list(filter(None, settings))

    # transform settings into dictionary
    settings_dict = {}
    
    for e in settings:
        # key
        pattern = re.compile("\"([^.*\"]*)\":")
        key = pattern.finditer(e)
        for i in key:
            key = i.group(1)
        
        # value
        pattern = re.compile("\:\s*\"([^.*\"]*)\"")
        value = pattern.finditer(e)
        for i in value:
            value = i.group(1)
        
        settings_dict.update({key: value})
    
    return settings_dict[key_name]


# get contents (i.e. of "include, "match" & "exclude")
def __get_contents__(name, text):
    pattern = re.compile("\""+name+"\":\s\{\s*([\n a-zA-Z0-9._-]+)\s*\}")
    contents = pattern.finditer(text)
    
    for e in contents:
        contents = e.group(1).replace("\t", "").replace(" ", "").split("\n")
    
    contents = list(filter(None, contents))
    return contents


# get a list of all files which require a back-up
def get_backup_files_list():
    with open(".config", "r") as file:
        config_text = file.read()
 
    match   = __get_contents__("match", config_text)
    include = __get_contents__("include", config_text)
    exclude = __get_contents__("exclude", config_text)

    # gets a list of all the files which require a back-up
    files_path = "files"
    files = [f for f in listdir(files_path) if isfile(join(files_path, f))]

    files_to_backup = []

    # match
    for e in match:
        for file in files:
            if file.__contains__(e):
                files_to_backup.append(file)

    # include
    for e in include:
        for file in files:
            if file == e:
                files_to_backup.append(e)
    files_to_backup = list(dict.fromkeys(files_to_backup))

    # exclude
    for e in exclude:
        for file in files:
            if file == e:
                files_to_backup.remove(e)

    print(files_to_backup)
    
    return files_to_backup