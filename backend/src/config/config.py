# Configuration settings for the application and database

import os

class MySQLConfig:
    HOST = os.getenv("MYSQL_HOST", "localhost")
    PORT = int(os.getenv("MYSQL_PORT", 3306))
    USER = os.getenv("MYSQL_USER", "root")
    PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
    DATABASE = os.getenv("MYSQL_DATABASE", "mydatabase")