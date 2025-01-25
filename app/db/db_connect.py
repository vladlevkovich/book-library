import asyncpg
import os

async def db_connect(test=False):
    if test:
        conn = await asyncpg.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('TEST_DATABASE'), host=os.getenv('BD_HOST'), port=os.getenv('DB_PORT'))
        try:
            return conn
        except Exception as e:
            return e
    else:
        conn = await asyncpg.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DATABASE'), host=os.getenv('BD_HOST'), port=os.getenv('DB_PORT'))
        try:
            return conn
        except Exception as e:
            return e
        # finally:
        #     await conn.close()
