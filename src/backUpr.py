#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join

# reads all settings and converts them into convenient lists
def get_contents(tag_name, text):
    content = []
    head = False
    body = False
    
    for line in text:
        if line.strip():
            if line.__contains__("}") and head == True and body == True:
                head = False
                body = False
        
            if head == True and body == True:
                content.append(line.strip())
            
            if line.__contains__("\""+tag_name+"\":") and head == False and body == False:
                head = True
            if line.__contains__("{") and head == True and body == False:
                body = True
    
    return content

def get_backup_files_list():
    config = open(".config", "r")
    config_text = config.readlines()
    config.close()
        
    match   = get_contents("match", config_text)
    include = get_contents("include", config_text)
    exclude = get_contents("exclude", config_text)


    # gets a list of all the files which require a back-up
    files_path = "files"
    files = [f for f in listdir(files_path) if isfile(join(files_path, f))]

    files_to_backup = []

    # match
    for element in match:
        for file in files:
            if file.__contains__(element):
                files_to_backup.append(file)

    # include
    for element in include:
        for file in files:
            if file == element:
                files_to_backup.append(element)
    files_to_backup = list(dict.fromkeys(files_to_backup))

    # exclude
    for element in exclude:
        for file in files:
            if file == element:
                files_to_backup.remove(element)

    return files_to_backup
