#!/usr/bin/env python3
import datetime
import os
import mysql.connector


# Database connection to create, delete and work with backups on the database
# Every function that changes the database except setup has the option to enable or disable commit
class DBConnection:

    # Establishes a connection to a database and sets up a cursor to work with
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )
        self.cursor = self.connection.cursor()

    # returns the connection
    def get_connection(self):
        return self.connection

    # returns the cursor for custom MySQL statements
    def get_cursor(self):
        return self.cursor

    # closes the connection to the database
    def close(self):
        self.cursor.close()
        self.connection.close()

    # sets up tables needed for backups if they don't already exist
    def setup(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS backups (id INT AUTO_INCREMENT PRIMARY KEY, creation_date "
                            "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, is_deleted BOOL NOT NULL DEFAULT 0, "
                            "success BOOL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS backup_files (id INT AUTO_INCREMENT PRIMARY KEY,"
                            " filepath VARCHAR(255) NOT NULL,"
                            " filename VARCHAR(255) NOT NULL, file LONGBLOB NOT NULL, size INT NOT NULL,"
                            " upload_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,"
                            " is_deleted BOOL NOT NULL DEFAULT 0, backup_id INT,"
                            " CONSTRAINT FK_backups FOREIGN KEY (backup_id) REFERENCES backups(id) ON DELETE CASCADE)")

    # deletes the created tables needed for backups
    def delete_tables(self, commit=False):
        self.cursor.execute('DROP TABLE IF EXISTS backup_files')
        self.cursor.execute('DROP TABLE IF EXISTS backups')
        if commit is True:
            self.connection.commit()

    # creates an empty backup and returns the id
    def create_backup(self, commit=False):
        self.cursor.execute('INSERT INTO backups (creation_date, is_deleted) VALUES(DEFAULT, DEFAULT)')
        row_id = self.cursor.lastrowid
        if commit is True:
            self.connection.commit()
        return row_id

    # returns a backup with the option to show deleted backups
    def get_backup(self, backup_id, show_deleted=False):
        select_query = """SELECT * FROM backups WHERE id = %s"""

        if show_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (backup_id,))
        return self.cursor.fetchall()

    # returns all backups with the option to show deleted backups
    def get_all_backups(self, show_deleted=False):
        select_query = """SELECT * FROM backups"""
        if show_deleted is False:
            select_query += " WHERE is_deleted = 0"

        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    # returns the size of a backup in bytes with the option to include deleted files
    def get_backup_size(self, backup_id, with_deleted=False):
        select_query = """SELECT SUM(size) FROM backup_files WHERE backup_id = %s"""

        if with_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (backup_id,))
        return (self.cursor.fetchall())[0]

    def get_last_backup_date(self, with_deleted=False):
        select_query = """SELECT MAX(creation_date) FROM backups"""

        if with_deleted is False:
            select_query += " WHERE is_deleted = 0"

        self.cursor.execute(select_query)
        date = (self.cursor.fetchall())[0]
        return date[0]

    # inserts a file into a backup on the database
    def insert_file(self, filepath: str, backup, commit=False):
        file = open(filepath, 'rb')

        insert_query = """ INSERT INTO backup_files (filepath, filename, file, size, backup_id)
         VALUES (%s, %s, %s, %s, %s)"""
        blob_tuple = (file.name, os.path.basename(file.name), file.read(), file.__sizeof__(), backup)

        self.cursor.execute(insert_query, blob_tuple)
        if commit is True:
            self.connection.commit()

    # returns a file with the option to show deleted files
    def get_file(self, file_id, show_deleted=False):
        select_query = """SELECT * FROM backup_files WHERE id = %s"""

        if show_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (file_id,))
        return self.cursor.fetchall()

    # returns all files with the option to show deleted files
    def get_all_files(self, show_deleted=False):
        select_query = """SELECT * FROM backup_files"""
        if show_deleted is False:
            select_query += " WHERE is_deleted = 0"

        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    # returns all files from a selected backup with the option to include deleted files
    def get_files_from_backup(self, backup_id, show_deleted=False):
        select_query = """SELECT * FROM backup_files WHERE backup_id = %s"""

        if show_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (backup_id,))
        return self.cursor.fetchall()

    # returns the size of a file in bytes with the option to include deleted files
    def get_file_size(self, file_id, with_deleted=False):
        select_query = "SELECT size FROM backup_files WHERE id=%s"

        if with_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (file_id,))
        return (self.cursor.fetchall())[0]

    # takes a list of file paths and creates a backup with all files in the list
    def create_backup_with_files(self, file_list, commit=False):
        backup_id = self.create_backup()
        for file in file_list:
            self.insert_file(file, backup_id)
        if commit is True:
            self.connection.commit()

    # deletes a backup and all associated files
    def delete_backup(self, backup_id, commit=False):
        delete_backup_query = """UPDATE backups SET is_deleted = 1 WHERE id = %s"""
        self.cursor.execute(delete_backup_query, (backup_id,))
        self.delete_files(backup_id=backup_id)
        if commit is True:
            self.connection.commit()
        return

    # deletes files from the database with different options to target files. All options stack together with an AND
    # relation
    def delete_files(self, file_id=None, backup_id=None, path=None, filename=None, commit=False):
        delete_file_query = """UPDATE backup_files SET is_deleted = 1 WHERE 1 = 1"""
        delete_tuple = ()
        if file_id is not None:
            delete_file_query += " AND id = %s"
            delete_tuple = delete_tuple + (file_id,)

        if backup_id is not None:
            delete_file_query += " AND backup_id = %s"
            delete_tuple = delete_tuple + (backup_id,)

        if path is not None:
            delete_file_query += " AND filepath LIKE %s"
            delete_tuple = delete_tuple + (path,)

        if filename is not None:
            delete_file_query += " AND filename LIKE %s"
            delete_tuple = delete_tuple + (filename,)

        self.cursor.execute(delete_file_query, delete_tuple)

        if commit is True:
            self.connection.commit()

    # deletes all files that were uploaded before a certain date
    def delete_files_before_date(self, date: datetime, commit=False):
        date_string = date.strftime('%Y-%m-%d %H:%M:%S')
        delete_query = """UPDATE backup_files SET is_deleted = 1 WHERE upload_date <= %s"""
        date_tuple = (date_string,)

        self.cursor.execute(delete_query, date_tuple)
        if commit is True:
            self.connection.commit()

    # deletes all backups that were created before a certain date
    def delete_backups_before_date(self, date: datetime, commit=False):
        date_string = date.strftime('%Y-%m-%d %H:%M:%S')
        select_query = """SELECT id FROM backups WHERE creation_date <= %s"""
        date_tuple = (date_string,)
        self.cursor.execute(select_query, date_tuple)
        ids = self.cursor.fetchall()
        if len(ids) == 0:
            return
        for element in ids:
            self.delete_backup(element[0])

        if commit is True:
            self.connection.commit()

    # permanently deletes all database entries that were set to deleted
    def permanently_clear_deleted_items(self, commit=True):
        delete_backup_files_query = """DELETE FROM backup_files WHERE is_deleted=1"""
        delete_backups_query = """DELETE FROM backups WHERE is_deleted=1"""
        self.cursor.execute(delete_backup_files_query)
        self.cursor.execute(delete_backups_query)

        if commit is True:
            self.connection.commit()

    # permanently deletes all database entries that were set to deleted and created before a certain date
    def permanently_clear_deleted_items_before_date(self, date: datetime, commit=True):
        date_string = date.strftime('%Y-%m-%d %H:%M:%S')
        date_tuple = (date_string,)
        delete_backup_files_query = """DELETE FROM backup_files WHERE is_deleted=1 AND upload_date <= %s"""
        delete_backups_query = """DELETE FROM backups WHERE is_deleted=1 AND creation_date <= %s"""
        self.cursor.execute(delete_backup_files_query, date_tuple)
        self.cursor.execute(delete_backups_query, date_tuple)

        if commit is True:
            self.connection.commit()
