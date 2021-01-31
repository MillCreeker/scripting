#!/usr/bin/env python3
from datetime import datetime
from datetime import timedelta

import Config as config
from DBConnection import DBConnection
import os
from Logger import Logger


def create_connection():
    host = config.get_config("database-settings", "host")
    if host is False or host is None:
        logger = Logger.get_instance()
        logger.err("Value \"host\" must not be None")
        return False
    
    user = config.get_config("database-settings", "user")
    if user is False or user is None:
        logger = Logger.get_instance()
        logger.err("Value \"user\" must not be None")
        return False
    
    password = config.get_config("database-settings", "password")
    if password is False:
        logger = Logger.get_instance()
        logger.err("Value \"password\" has not been declared in file.config")
        return False
    
    database = config.get_config("database-settings", "database")
    if database is False or database is None:
        logger = Logger.get_instance()
        logger.err("Value \"database\" must not be None")
        return False

    return DBConnection(host, user, password, database)

os.chdir("..")
logger = Logger.get_instance()

connection = create_connection()

# checks whetther connection received valid values
if connection is False:
    exit(1)

connection.setup()

file_list = config.get_backup_files_list()

last_backup_date = connection.get_last_backup_date()
if last_backup_date:
    last_backup_date = last_backup_date.replace(hour=0, minute=0, second=0, microsecond=0)

current_date = datetime.now()


# checks whether the back-up specifications are valid
backup_frequency = int(config.get_config("settings", "backup-frequency"))
if backup_frequency is False or backup_frequency < 0:
    logger.err("Please enter a valid value for \"backup-frequency\"")
    exit(1)

delete_after = int(config.get_config("settings", "delete-after"))
if delete_after < 0:
    logger.err("Please enter a valid value for \"delete-after\"")
    exit(1)

permanent_delete = int(config.get_config("settings", "permanent-delete"))
if permanent_delete is False or permanent_delete <0:
    logger.err("Please enter a valid value for \"permanent-delete\"")
    exit(1)



if last_backup_date is None or last_backup_date < (current_date - timedelta(days=backup_frequency)):
    connection.create_backup_with_files(file_list, True)

connection.delete_backups_before_date(date=((current_date - timedelta(days=delete_after)).replace(hour=23, minute=59, second=59, microsecond=59)), commit=True)
connection.permanently_clear_deleted_items_before_date(date=((current_date - timedelta(days=permanent_delete)).replace(hour=23, minute=59, second=59, microsecond=59)), commit=True)

connection.close()

exit(0)