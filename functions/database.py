import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

mysql_config = {
    'host': os.environ.get("DBhost"),
    'user': os.environ.get("DBuser"),
    'password': os.environ.get("DBpass"),
    'database': os.environ.get("DBname"),
}

def create_tables():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    tables = {
        'wallet': '''
            CREATE TABLE IF NOT EXISTS wallet (
                user_id BIGINT PRIMARY KEY,
                coins INT
            )
        ''',
        'bank': '''
            CREATE TABLE IF NOT EXISTS bank (
                user_id BIGINT PRIMARY KEY,
                coins INT
            )
        ''',
        'loans': '''
            CREATE TABLE IF NOT EXISTS loans (
                loan_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT,
                amount INT,
                status VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES wallet(user_id)
            )
        ''',
        'cooldowns': '''
            CREATE TABLE IF NOT EXISTS cooldowns (
                user_id BIGINT PRIMARY KEY,
                last_used TIMESTAMP
            )
        ''',
        'verification_channels': '''
            CREATE TABLE IF NOT EXISTS verification_channels (
                guild_id BIGINT,
                channel_id BIGINT PRIMARY KEY,
                role_id BIGINT
            )
        '''
    }

    for table, query in tables.items():
        cursor.execute(query)

    conn.commit()
    conn.close()

def initialize_database():
    create_tables()