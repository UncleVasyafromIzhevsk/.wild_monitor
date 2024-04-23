import os
import asyncio

from aiogram import Bot, types
from aiogram.utils.media_group import MediaGroupBuilder

from dotenv import load_dotenv

from productStatistics import product_statistics

# Получение переменных
load_dotenv()
token_tg = os.getenv("TOKEN_TG")
bot = Bot(token=token_tg)


# Отправка сообщений пользователю
# Сообщение об удалении товара из-за его отсутствия
async def product_out_stock(**kwargs):
    user_id = kwargs['user_id']
    goods = kwargs['goods']
    link_picture = kwargs['link_picture']
    await bot.send_photo(
        user_id, photo=link_picture, caption=f'{goods} - нет в наличии на ВБ, товар удален')


# Сообщение об изменении цены на товар
async def price_change(**kwargs):
    user_id = kwargs['user_id']
    goods = kwargs['goods']
    link_picture = kwargs['link_picture']
    file_picture = types.FSInputFile(kwargs['file_picture'])
    link_goods = kwargs['link_goods']
    starting_price = kwargs['starting_price']
    last_price = kwargs['last_price']
    percent = product_statistics.percent_change(
        starting_price=starting_price,
        last_price=last_price
    )
    # Собираем альбом
    album_builder = MediaGroupBuilder(
        caption=f'{goods}\nЦена изменилась на: {percent}\nСсылка на товар:\n{link_goods}'
    )
    album_builder.add(
        type="photo",
        media=file_picture
    )
    # Если мы сразу знаем тип, то вместо общего add
    # можно сразу вызывать add_<тип>
    album_builder.add_photo(
        # Для ссылок или file_id достаточно сразу указать значение
        media=link_picture
    )
    await bot.send_media_group(
        user_id, media=album_builder.build())

# asyncio.run(
#     price_change(
#         user_id=5369585473,
#         goods='Зарядное устройство телефона,зарядка type-c быстрая блок',
#         link_picture='https://basket-02.wbbasket.ru/vol147/part14747/14747989/images/big/1.webp',
#         file_picture='product_statis.png',
#         link_goods='https://www.wildberries.ru/catalog/14747989/detail.aspx',
#         starting_price=2234,
#         last_price=3420
#     )
# )