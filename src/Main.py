#!/usr/bin/env python3
import src.Config as config
from src.DBConnection import DBConnection
from src.logger import logger


def create_connection():
    host = config.get_config("database-settings", "host")
    user = config.get_config("database-settings", "user")
    password = config.get_config("database-settings", "password")
    database = config.get_config("database-settings", "database")

    return DBConnection(host, user, password, database)


logger = logger.__getattr__()

connection = create_connection()
connection.setup()

file_list = config.get_backup_files_list()

connection.create_backup_with_files(file_list, True)
