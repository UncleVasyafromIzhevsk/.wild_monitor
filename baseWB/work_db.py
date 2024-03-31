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
    try:
        async with aiosqlite.connect('./baseWB/baseWB.db') as db:
            async with db.execute(
                    'SELECT user_id FROM user') as cursor:
                user_id = await cursor.fetchall()
                list_id = []
                for a in user_id:
                    list_id.append(a[0])
                if args[0] in list_id:
                    await db.commit()
                    return False
                else:
                    await db.execute(
                        "INSERT INTO user VALUES(?,?);", args
                    )
                    await db.commit()
                    return True
    except Exception as e:
        print(
            f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}")
#asyncio.run(add_user(1, 'ЖИГА'))

# Удаление пользователи и его данных из БД
async def delete_user(*args):
    try:
        async with aiosqlite.connect('./baseWB/baseWB.db') as db:
            async with db.execute(
                    'SELECT user_id FROM user') as cursor:
                user_id = await cursor.fetchall()
                list_id = []
                for a in user_id:
                    list_id.append(a[0])
                if args[0] in list_id:
                    # Удаление пользователя до этого надо сделать
                    # удаление всех его товаров
                    await db.execute(
                        "DELETE FROM user WHERE user_id=?", (args)
                    )
                    await db.commit()
                    return True
                else:
                    await db.commit()
                    return False
    except Exception as e:
        print(
            f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}")
#asyncio.run(delete_user(5369585473))
