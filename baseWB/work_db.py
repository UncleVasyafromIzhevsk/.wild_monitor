import aiosqlite
import asyncio

from wbAPI import wbapi


# Создание или проверка существования БД
# Создание таблицы пользователей
# Создание таблицы товаров
async def create_table():
    async with aiosqlite.connect('./baseWB/baseWB.db') as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS user(
                    user_id INTEGER PRIMARY KEY, name TEXT);"""
        )
        await db.execute(
            """CREATE TABLE IF NOT EXISTS goods(
                    user_id INTEGER, article INTEGER, name TEXT, starting_price REAL,
                    registration_date TEXT, link_picture TEXT, link_goods TEXT, goods_table_name TEXT);"""
        )
        await db.commit()


# asyncio.run(create_table())

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


# asyncio.run(add_user(1, 'ЖИГА'))

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
                    await del_goods_db(args[0], 0, 'user_id')
                    # удаление всех его товаров
                    await db.execute(
                        "DELETE FROM user WHERE user_id=?", args
                    )
                    await db.commit()
                    return True
                else:
                    await db.commit()
                    return False
    except Exception as e:
        print(
            f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}")


# asyncio.run(delete_user(5369585473))

# Внесение товара в БД
async def add_goods_db(*args):
    user_id = args[0]
    article = int(args[1])
    name = args[2]
    starting_price = args[3]
    registration_date = args[4]
    link_picture = args[5]
    link_goods = args[6]
    goods_table_name = ('index' + str(args[0]) + str(args[1]))
    try:
        async with aiosqlite.connect('./baseWB/baseWB.db') as db:
            # Проверка на наличие товара в БД
            async with db.execute(
                    'SELECT user_id, article FROM goods') as cursor:
                list_id_art = await cursor.fetchall()
                list_reference = [user_id, article]
                for a in list_id_art:
                    print(list(a))
                    print(list_reference)
                    if list(a) == list_reference:
                        print('huy')
                        await db.commit()
                        return False
            # Добавление товара
            async with db.execute(
                    'INSERT INTO goods(user_id, article, name, starting_price, registration_date,'
                    'link_picture, link_goods, goods_table_name)VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (
                            user_id, article, name, starting_price, registration_date, link_picture, link_goods,
                            goods_table_name
                    )
            ) as cursor:
                # Добавление таблицы товара для цены и времени изменения цены
                await db.execute(
                    f'CREATE TABLE IF NOT EXISTS {goods_table_name}(data TEXT, last_price REAL);'
                )
                # Добавление начального времени и цены в таблицу товара
                await db.execute(
                    f'INSERT INTO {goods_table_name}(data, last_price)VALUES (?, ?)', (
                        registration_date, starting_price
                    )
                )
                await db.commit()
                return True
    except Exception as e:
        print(
            f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}")
        return None


#asyncio.run(add_goods_db(114, 111, 'gjpf', 11.1, 'data', 'https://rob.ru', 'https://top.ru'))

# Удаление товара в БД
async def del_goods_db(*args):
    user_id = args[0]
    article = args[1]
    select_d = args[2]
    goods_table_name = ('index' + str(args[0]) + str(args[1]))
    try:
        # Удаление одного товара по артикулу и его юзеру
        if select_d == 'article':
            async with aiosqlite.connect('./baseWB/baseWB.db') as db:
                async with db.execute(
                        'DELETE from goods where user_id = ? AND article = ?', (
                            user_id, article
                        )
                ) as cursor:
                    # Удаление таблицы товара
                    await db.execute(
                        f'DROP TABLE IF EXISTS {goods_table_name};'
                    )
                    await db.commit()
                    return True
        # Удаление всех товаров пользователя при удалении его бд
        if select_d == 'user_id':
            async with aiosqlite.connect('./baseWB/baseWB.db') as db:
                async with db.execute(
                        f'SELECT user_id, goods_table_name from goods'
                ) as cursor:
                    list_id = await cursor.fetchall()
                    for a in list_id:
                        if user_id == a[0]:
                            # Удаление таблиц товаров
                            await db.execute(
                                f'DROP TABLE IF EXISTS {a[1]};'
                            )
                            # Удаление товаров из таблицы товаров
                            await db.execute(
                                f'DELETE from goods where user_id = {a[0]};'
                            )
                    await db.commit()
                    return True
    except Exception as e:
        print(
            f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}")
        return False


#asyncio.run(del_goods_db(112, 111, 'user_id'))

# Опрос цен и отправка отчетов (главный цикл)
async def product_survey():
    try:
        async with aiosqlite.connect('baseWB.db') as db: #./baseWB/baseWB.db') as db:
            async with db.execute(
                    'SELECT user_id, name FROM user'
            ) as cursor:
                # Перебор пользователей
                list_id_name = await cursor.fetchall()
                for user in list_id_name:
                    user_id = user[0]
                    user_name = user[1]
                    print('\n', '\n', user_id, user_name, '\n')
                    # Перебор товаров пользователя
                    async with db.execute(
                            f'SELECT article, starting_price, link_picture,'
                            f'goods_table_name, name FROM goods '
                            f'WHERE user_id LIKE "{user_id}";'
                    ) as cursor_goods:
                        list_goods = await cursor_goods.fetchall()
                        for good in list_goods:
                            article = good[0]
                            starting_price = good[1]
                            link_picture = good[2]
                            goods_table_name = good[3]
                            goods_name = good[4]
                            # print(article, '\n',starting_price, '\n', link_picture, '\n', goods_table_name,
                            #       '\n', goods_name, '\n')
                            # Опрос цены и наличия
                            new_product_data = await wbapi.get_current_price(str(article))
                            print(new_product_data['name'], '\n',
                                  new_product_data['price'], ' руб', '\n',
                                  'Наличие: ', new_product_data['is_available'], '\n')

    except Exception as e:
        print(
            f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}, 'В цикле опроса цен'")

asyncio.run(product_survey())

