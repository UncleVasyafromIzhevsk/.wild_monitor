import aiosqlite
import asyncio

# Создание или проверка существования БД
# Создание таблицы пользователей
async def create_table():
    async with aiosqlite.connect('baseWB.db') as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS user(
                    user_id INTEGER PRIMARY KEY, name TEXT);"""
        )
        await db.commit()
#asyncio.run(create_table())

# Поиск пользователя в таблице и при его отсутствии его добавление
async def add_user(*args):
    async with aiosqlite.connect('baseWB.db') as db:
        async with db.execute(
                'SELECT user_id FROM user') as cursor:
            user_id = await cursor.fetchall()
            print(args[0])
            for a in user_id:
                print(a[0])
                if args[0] == a[0]:
                    print('kuy')
                    return False
                else:
                    await db.execute(
                        "INSERT INTO user VALUES(""?,?);", args
                    )
                print(user_id)
        await db.commit()
asyncio.run(add_user(3, 'gena'))

