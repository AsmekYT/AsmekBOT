import os
import mysql.connector
import mysql.connector.pooling
import asyncio
import logging
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

mysql_config = {
    'host': os.environ.get("DBhost"),
    'user': os.environ.get("DBuser"),
    'password': os.environ.get("DBpass"),
    'database': os.environ.get("DBname"),
    'pool_name': 'asmekbot_pool',
    'pool_size': 5,
    'autocommit': True
}

db_pool = None

def initialize_database():
    global db_pool
    try:
        conn_test = mysql.connector.connect(
            host=mysql_config['host'],
            user=mysql_config['user'],
            password=mysql_config['password']
        )
        cursor_test = conn_test.cursor()
        cursor_test.execute(f"CREATE DATABASE IF NOT EXISTS {mysql_config['database']}")
        cursor_test.close()
        conn_test.close()
        log.info(f"Database '{mysql_config['database']}' checked/created.")

        db_pool = mysql.connector.pooling.MySQLConnectionPool(**mysql_config)
        log.info(f"Database connection pool '{mysql_config['pool_name']}' initialized with size {mysql_config['pool_size']}.")

        conn = db_pool.get_connection()
        cursor = conn.cursor()

        tables = {
            'economy': '''
                CREATE TABLE IF NOT EXISTS economy (
                    user_id BIGINT PRIMARY KEY,
                    wallet_coins INT DEFAULT 0,
                    bank_coins INT DEFAULT 0,
                    work_last_used TIMESTAMP NULL DEFAULT NULL,
                    slut_last_used TIMESTAMP NULL DEFAULT NULL,
                    crime_last_used TIMESTAMP NULL DEFAULT NULL,
                    xp INT DEFAULT 0,
                    loans INT DEFAULT 0,
                    loan_amount INT DEFAULT 0,
                    loan_status VARCHAR(255) DEFAULT NULL
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

        for table_name, query in tables.items():
            try:
                cursor.execute(query)
                log.info(f"Table '{table_name}' checked/created successfully.")
            except mysql.connector.Error as err:
                log.error(f"Failed creating/checking table {table_name}: {err}")

        cursor.close()
        conn.close()
        log.info("Database tables checked/created.")

    except mysql.connector.Error as err:
        log.error(f"Database initialization failed: {err}")
        db_pool = None
    except Exception as e:
        log.error(f"An unexpected error occurred during database initialization: {e}")
        db_pool = None


async def fetchone(query: str, params: tuple = None):
    if not db_pool:
        log.error("Database pool is not initialized.")
        return None
    conn = None
    cursor = None
    loop = asyncio.get_event_loop()
    try:
        conn = await loop.run_in_executor(None, db_pool.get_connection)
        cursor = await loop.run_in_executor(None, conn.cursor)
        await loop.run_in_executor(None, cursor.execute, query, params)
        result = await loop.run_in_executor(None, cursor.fetchone)
        return result
    except mysql.connector.Error as err:
        log.error(f"Database fetchone error: {err}. Query: {query}, Params: {params}")
        return None
    except Exception as e:
        log.error(f"Unexpected error during fetchone: {e}")
        return None
    finally:
        if cursor:
            await loop.run_in_executor(None, cursor.close)
        if conn and conn.is_connected():
             await loop.run_in_executor(None, conn.close)

async def fetchall(query: str, params: tuple = None):
    if not db_pool:
        log.error("Database pool is not initialized.")
        return None
    conn = None
    cursor = None
    loop = asyncio.get_event_loop()
    try:
        conn = await loop.run_in_executor(None, db_pool.get_connection)
        cursor = await loop.run_in_executor(None, conn.cursor)
        await loop.run_in_executor(None, cursor.execute, query, params)
        result = await loop.run_in_executor(None, cursor.fetchall)
        return result
    except mysql.connector.Error as err:
        log.error(f"Database fetchall error: {err}. Query: {query}, Params: {params}")
        return None
    except Exception as e:
        log.error(f"Unexpected error during fetchall: {e}")
        return None
    finally:
        if cursor:
            await loop.run_in_executor(None, cursor.close)
        if conn and conn.is_connected():
             await loop.run_in_executor(None, conn.close)

async def execute(query: str, params: tuple = None):
    if not db_pool:
        log.error("Database pool is not initialized.")
        return False
    conn = None
    cursor = None
    loop = asyncio.get_event_loop()
    try:
        conn = await loop.run_in_executor(None, db_pool.get_connection)
        cursor = await loop.run_in_executor(None, conn.cursor)
        await loop.run_in_executor(None, cursor.execute, query, params)
        return True
    except mysql.connector.Error as err:
        log.error(f"Database execute error: {err}. Query: {query}, Params: {params}")
        return False
    except Exception as e:
        log.error(f"Unexpected error during execute: {e}")
        return False
    finally:
        if cursor:
            await loop.run_in_executor(None, cursor.close)
        if conn and conn.is_connected():
            await loop.run_in_executor(None, conn.close)