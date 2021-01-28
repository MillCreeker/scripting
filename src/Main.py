#!/usr/bin/env python3
from datetime import datetime
from datetime import timedelta

import src.Config as config
from src.DBConnection import DBConnection
import os
#from src.logger import logger


def create_connection():
    host = config.get_config("database-settings", "host")
    user = config.get_config("database-settings", "user")
    password = config.get_config("database-settings", "password")
    database = config.get_config("database-settings", "database")

    return DBConnection(host, user, password, database)

os.chdir("..")
#logger = logger.__getattr__()

connection = create_connection()
connection.setup()

file_list = config.get_backup_files_list()

last_backup_date = connection.get_last_backup_date()
last_backup_date = last_backup_date.replace(hour=0, minute=0, second=0, microsecond=0)
current_date = datetime.now()
backup_frequency = int(config.get_config("settings", "backup-frequency"))
delete_after = int(config.get_config("settings", "delete-after"))
permanent_delete = int(config.get_config("settings", "permanent-delete"))

if last_backup_date < (current_date - timedelta(days=backup_frequency)):
    connection.create_backup_with_files(file_list, True)

connection.delete_backups_before_date(date=((current_date - timedelta(days=delete_after)).replace(hour=23, minute=59, second=59, microsecond=59)), commit=True)
connection.permanently_clear_deleted_items_before_date(date=((current_date - timedelta(days=permanent_delete)).replace(hour=23, minute=59, second=59, microsecond=59)), commit=True)

