import mysql.connector

class DBConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="backupr"
        )
        self.cursor = self.connection.cursor()

    def get_connection(self):
        return self.connection

    def setup(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS backup_files (id INT AUTO_INCREMENT PRIMARY KEY, filename "
                            "VARCHAR(255) NOT NULL, file LONGBLOB NOT NULL, size INT NOT NULL,"
                            " upload_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,"
                            " is_deleted BOOL NOT NULL DEFAULT 0, backup_id INT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS backups (id INT AUTO_INCREMENT PRIMARY KEY, creation_date "
                            "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, is_deleted BOOL NOT NULL DEFAULT 0, "
                            "success BOOL)")
        self.cursor.execute("ALTER TABLE backup_files ADD CONSTRAINT FK_backups FOREIGN KEY (backup_id) REFERENCES "
                            "backups(id)")
