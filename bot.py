import asyncio
import os

from aiogram import Bot, Dispatcher, types, methods, Router
from aiogram.client.session.middlewares.base import NextRequestMiddlewareType
from aiogram.methods.base import TelegramType, TelegramMethod
from aiogram.client.session.middlewares.request_logging import RequestLogging

from dotenv import load_dotenv

from userCom import user_com
from baseWB import work_db

# Получение переменых
load_dotenv()
token_tg = os.getenv("TOKEN_TG")


# Запуск бота
async def main():
    bot = Bot(token=token_tg)
    dp = Dispatcher()

    # Подключение хендлеров
    dp.include_routers(user_com.router)

    # Запускаем бота и пропускаем все накопленные
    # входящие
    # Да, этот метод можно вызвать даже если у вас
    # поллинг
    await bot.delete_webhook(drop_pending_updates=True)

    # Запуск поллинг в on_startup устанвливаем конкурентные корутины
    # await dp.start_polling(bot)
    await dp.start_polling(bot, skip_updates=False,
                           on_startup=(
                               # Асинхронное создание БД и таблиц или их проверка
                               asyncio.create_task(work_db.create_table()),
                               # Проверка цен на товары в БД
                               asyncio.create_task(work_db.product_survey()),
                               #                            # Обновление цен в бесконечном цикле
                               #                            asyncio.create_task(
                               #                                tinBase.get_lates_prices()),
                               #                            # Прогон табуна из 4 коней в бесконечном цикле
                               #                            asyncio.create_task(
                               #                                single_horse_one.hippodrome(bot)),
                               #                            asyncio.create_task(
                               #                                single_horse_two.hippodrome(bot)),
                               #                            asyncio.create_task(
                               #                                single_horse_tree.hippodrome(bot)),
                               #                            asyncio.create_task(
                               #                                single_horse_four.hippodrome(bot)),
                           )
                           )


if __name__ == "__main__":
    asyncio.run(main())
