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
        'user_data': '''
            CREATE TABLE IF NOT EXISTS economy (
                user_id BIGINT PRIMARY KEY,
                wallet_coins INT,
                bank_coins INT,
                work_last_used TIMESTAMP NULL DEFAULT NULL,
                slut_last_used TIMESTAMP NULL DEFAULT NULL,
                crime_last_used TIMESTAMP NULL DEFAULT NULL,
                xp INT,
                loans INT,
                loan_amount INT,
                loan_status VARCHAR(255)
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