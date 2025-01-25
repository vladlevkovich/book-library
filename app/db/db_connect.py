import asyncpg

async def db_connect(test=False):
    if test:
        conn = await asyncpg.connect(user='postgres', password='admin', database='test_books', host='localhost', port=5432)
        try:
            return conn
        except Exception as e:
            return e
    else:
        conn = await asyncpg.connect(user='postgres', password='admin', database='books', host='localhost', port=5432)
        try:
            return conn
        except Exception as e:
            return e
        # finally:
        #     await conn.close()
