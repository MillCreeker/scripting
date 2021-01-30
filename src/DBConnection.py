#!/usr/bin/env python3
import datetime
import os
import mysql.connector
from Logger import Logger


# Database connection to create, delete and work with backups on the database
# Every function that changes the database except setup has the option to enable or disable commit
class DBConnection:

    # Establishes a connection to a database and sets up a cursor to work with
    def __init__(self, host, user, password, database):
        self.logger = Logger.get_instance()
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )
            self.cursor = self.connection.cursor()
            self.logger.log('connection to database established')
        except:
            self.logger.err('failed to establish a connection to the database')
            exit(2)

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
        was_changed = False
        self.cursor.execute("""SELECT count(*) FROM information_schema.tables
            WHERE table_name = 'backups' OR table_name = 'backup_files'""")
        if self.cursor.fetchone()[0] < 2:
            was_changed = True
        self.cursor.execute("CREATE TABLE IF NOT EXISTS backups (id INT AUTO_INCREMENT PRIMARY KEY, creation_date "
                            "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, is_deleted BOOL NOT NULL DEFAULT 0, "
                            "success BOOL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS backup_files (id INT AUTO_INCREMENT PRIMARY KEY,"
                            " filepath VARCHAR(255) NOT NULL,"
                            " filename VARCHAR(255) NOT NULL, file LONGBLOB NOT NULL, size INT NOT NULL,"
                            " upload_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,"
                            " is_deleted BOOL NOT NULL DEFAULT 0, backup_id INT,"
                            " CONSTRAINT FK_backups FOREIGN KEY (backup_id) REFERENCES backups(id) ON DELETE CASCADE)")
        if was_changed:
            self.logger.log('created database tables for backup')

    # deletes the created tables needed for backups
    def delete_tables(self, commit=False):
        if commit:
            self.logger.log('transaction started')
        try:
            self.cursor.execute('DROP TABLE IF EXISTS backup_files')
            self.cursor.execute('DROP TABLE IF EXISTS backups')
            self.logger.log('deleted backup tables in database')
            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')
        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)

    # creates an empty backup and returns the id
    def create_backup(self, commit=False):
        if commit:
            self.logger.log('transaction started')
        try:
            self.cursor.execute('INSERT INTO backups (creation_date, is_deleted) VALUES(DEFAULT, DEFAULT)')
            row_id = self.cursor.lastrowid
            self.logger.log('backup created with id {}'.format(row_id))
            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')
            return row_id
        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)

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

    # returns the date of the last backup made
    def get_last_backup_date(self, with_deleted=False):
        select_query = """SELECT MAX(creation_date) FROM backups"""

        if with_deleted is False:
            select_query += " WHERE is_deleted = 0"

        self.cursor.execute(select_query)
        date = (self.cursor.fetchall())[0]
        return date[0]

    # inserts a file into a backup on the database
    def insert_file(self, filepath: str, backup, commit=False):
        if commit:
            self.logger.log('transaction started')
        try:
            file = open(filepath, 'rb')

            insert_query = """ INSERT INTO backup_files (filepath, filename, file, size, backup_id)
             VALUES (%s, %s, %s, %s, %s)"""
            blob_tuple = (file.name, os.path.basename(file.name), file.read(), file.__sizeof__(), backup)
            self.cursor.execute(insert_query, blob_tuple)
            self.logger.log('inserted file "{}" into backup {}'.format(os.path.basename(file.name), backup))
            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')

        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)

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
        if commit:
            self.logger.log('transaction started')
        try:
            backup_id = self.create_backup()
            for file in file_list:
                self.insert_file(file, backup_id)
            self.logger.log('all files backed up')
            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')
        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)

    # deletes a backup and all associated files
    def delete_backup(self, backup_id, commit=False):
        if commit:
            self.logger.log('transaction started')
        try:
            self.logger.log('deleting backup with id {}'.format(backup_id))
            delete_backup_query = """UPDATE backups SET is_deleted = 1 WHERE id = %s"""
            self.delete_files(backup_id=backup_id)
            self.cursor.execute(delete_backup_query, (backup_id,))
            self.logger.log('deleted backup with id {}'.format(backup_id))
            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')
        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)

    # deletes files from the database with different options to target files. All options stack together with an AND
    # relation
    def delete_files(self, file_id=None, backup_id=None, path=None, filename=None, commit=False):
        if commit:
            self.logger.log('transaction started')
        try:
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
            self.logger.log('deleted {} files'.format(self.cursor.rowcount))
            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')
        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)

    # deletes all files that were uploaded before a certain date
    def delete_files_before_date(self, date: datetime, commit=False):
        if commit:
            self.logger.log('transaction started')
        try:
            date_string = date.strftime('%Y-%m-%d %H:%M:%S')
            delete_query = """UPDATE backup_files SET is_deleted = 1 WHERE upload_date <= %s"""
            date_tuple = (date_string,)

            self.cursor.execute(delete_query, date_tuple)
            self.logger.log('deleted {} files that were created before {}'.format(self.cursor.rowcount, date))
            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')
        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)

    # deletes all backups that were created before a certain date
    def delete_backups_before_date(self, date: datetime, commit=False):
        if commit:
            self.logger.log('transaction started')
        try:
            date_string = date.strftime('%Y-%m-%d %H:%M:%S')
            select_query = """SELECT id FROM backups WHERE creation_date <= %s"""
            date_tuple = (date_string,)
            self.cursor.execute(select_query, date_tuple)
            ids = self.cursor.fetchall()
            self.logger.log('deleting {} backups before {}'.format(len(ids), date))
            no_backups_before_date = False
            if len(ids) == 0:
                no_backups_before_date = True
            if no_backups_before_date is False:
                for element in ids:
                    self.delete_backup(element[0])
            self.logger.log('deleted all backups before {}'.format(date))
            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')
        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)

    # permanently deletes all database entries that were set to deleted
    def permanently_clear_deleted_items(self, commit=True):
        if commit:
            self.logger.log('transaction started')
        try:
            delete_backup_files_query = """DELETE FROM backup_files WHERE is_deleted=1"""
            delete_backups_query = """DELETE FROM backups WHERE is_deleted=1"""
            self.cursor.execute(delete_backup_files_query)
            self.logger.log('permanently cleared {} files'.format(self.cursor.rowcount))
            self.cursor.execute(delete_backups_query)
            self.logger.log('permanently cleared {} backups'.format(self.cursor.rowcount))

            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')
        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)

    # permanently deletes all database entries that were set to deleted and created before a certain date
    def permanently_clear_deleted_items_before_date(self, date: datetime, commit=True):
        if commit:
            self.logger.log('transaction started')
        try:
            date_string = date.strftime('%Y-%m-%d %H:%M:%S')
            date_tuple = (date_string,)
            delete_backup_files_query = """DELETE FROM backup_files WHERE is_deleted=1 AND upload_date <= %s"""
            delete_backups_query = """DELETE FROM backups WHERE is_deleted=1 AND creation_date <= %s"""
            self.cursor.execute(delete_backup_files_query, date_tuple)
            self.logger.log('permanently cleared {} files before {}'.format(self.cursor.rowcount, date))
            self.cursor.execute(delete_backups_query, date_tuple)
            self.logger.log('permanently cleared {} backups before {}'.format(self.cursor.rowcount, date))

            if commit is True:
                self.connection.commit()
                self.logger.log('transaction finished')
        except:
            self.connection.rollback()
            self.logger.err('transaction failed and rolled back')
            self.close()
            exit(2)
