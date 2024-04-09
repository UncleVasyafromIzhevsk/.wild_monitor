import os

from aiogram import Bot

from dotenv import load_dotenv


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