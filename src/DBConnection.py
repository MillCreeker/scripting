import mysql.connector
import os
import binascii


class DBConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="backupr",
            use_pure=True
        )
        self.cursor = self.connection.cursor()

    def get_connection(self):
        return self.connection

    def close(self):
        self.cursor.close()
        self.connection.close()

    def setup(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS backups (id INT AUTO_INCREMENT PRIMARY KEY, creation_date "
                            "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, is_deleted BOOL NOT NULL DEFAULT 0, "
                            "success BOOL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS backup_files (id INT AUTO_INCREMENT PRIMARY KEY, filename "
                            "VARCHAR(255) NOT NULL, file LONGBLOB NOT NULL, size INT NOT NULL,"
                            " upload_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,"
                            " is_deleted BOOL NOT NULL DEFAULT 0, backup_id INT,"
                            " CONSTRAINT FK_backups FOREIGN KEY (backup_id) REFERENCES backups(id))")

    def create_backup(self):
        self.cursor.execute('INSERT INTO backups (creation_date, is_deleted) VALUES(DEFAULT, DEFAULT)')
        row_id = self.cursor.lastrowid
        self.connection.commit()
        return row_id

    def insert_file(self, filepath: str, backup):
        file = open(filepath, 'rb')

        insert_query = """ INSERT INTO backup_files (filename, file, size, backup_id) VALUES (%s, %s, %s, %s)"""
        blob_tuple = (os.path.basename(file.name), file.read(), file.__sizeof__(), backup)

        self.cursor.execute(insert_query, blob_tuple)
        self.connection.commit()
