import mysql.connector
import os
import binascii
import datetime


class DBConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="backupr",
        )
        self.cursor = self.connection.cursor()

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor

    def close(self):
        self.cursor.close()
        self.connection.close()

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

    def delete_tables(self, commit=False):
        self.cursor.execute('DROP TABLE IF EXISTS backup_files')
        self.cursor.execute('DROP TABLE IF EXISTS backups')
        if commit is True:
            self.connection.commit()

    def create_backup(self, commit=False):
        self.cursor.execute('INSERT INTO backups (creation_date, is_deleted) VALUES(DEFAULT, DEFAULT)')
        row_id = self.cursor.lastrowid
        if commit is True:
            self.connection.commit()
        return row_id

    def get_backup(self, backup_id, show_deleted=False):
        select_query = """SELECT * FROM backups WHERE id = %s"""

        if show_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (backup_id,))
        return self.cursor.fetchall()

    def get_all_backups(self, show_deleted=False):
        select_query = """SELECT * FROM backups"""
        if show_deleted is False:
            select_query += " WHERE is_deleted = 0"

        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def get_backup_size(self, backup_id, with_deleted=False):
        select_query = """SELECT SUM(size) FROM backup_files WHERE backup_id = %s"""

        if with_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (backup_id,))
        return (self.cursor.fetchall())[0]

    def insert_file(self, filepath: str, backup, commit=False):
        file = open(filepath, 'rb')

        insert_query = """ INSERT INTO backup_files (filepath, filename, file, size, backup_id)
         VALUES (%s, %s, %s, %s, %s)"""
        blob_tuple = (file.name, os.path.basename(file.name), file.read(), file.__sizeof__(), backup)

        self.cursor.execute(insert_query, blob_tuple)
        if commit is True:
            self.connection.commit()

    def get_file(self, file_id, show_deleted=False):
        select_query = """SELECT * FROM backup_files WHERE id = %s"""

        if show_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (file_id,))
        return self.cursor.fetchall()

    def get_all_files(self, show_deleted=False):
        select_query = """SELECT * FROM backup_files"""
        if show_deleted is False:
            select_query += " WHERE is_deleted = 0"

        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def get_files_from_backup(self, backup_id, show_deleted=False):
        select_query = """SELECT * FROM backup_files WHERE backup_id = %s"""

        if show_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (backup_id,))
        return self.cursor.fetchall()

    def get_file_size(self, file_id, with_deleted=False):
        select_query = "SELECT size FROM backup_files WHERE id=%s"

        if with_deleted is False:
            select_query += " AND is_deleted = 0"

        self.cursor.execute(select_query, (file_id,))
        return (self.cursor.fetchall())[0]

    def create_backup_with_files(self, file_list, commit=False):
        backup_id = self.create_backup()
        for file in file_list:
            self.insert_file(file, backup_id)
        if commit is True:
            self.connection.commit()

    def delete_backup(self, backup_id, commit=False):
        delete_backup_query = """UPDATE backups SET is_deleted = 1 WHERE id = %s"""
        self.cursor.execute(delete_backup_query, (backup_id,))
        self.delete_files(backup_id=backup_id)
        if commit is True:
            self.connection.commit()
        return

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

    def delete_files_before_date(self, date: datetime, commit=False):
        date_string = date.strftime('%Y-%m-%d %H:%M:%S')
        delete_query = """UPDATE backup_files SET is_deleted = 1 WHERE upload_date <= %s"""
        date_tuple = (date_string,)

        self.cursor.execute(delete_query, date_tuple)
        if commit is True:
            self.connection.commit()

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

    def permanently_clear_deleted_items(self, commit=True):
        delete_backup_files_query = """DELETE FROM backup_files WHERE is_deleted=1"""
        delete_backups_query = """DELETE FROM backups WHERE is_deleted=1"""
        self.cursor.execute(delete_backup_files_query)
        self.cursor.execute(delete_backups_query)

        if commit is True:
            self.connection.commit()
