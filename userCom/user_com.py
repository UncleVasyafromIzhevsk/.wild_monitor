import json
import os
import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message, ReplyKeyboardRemove, FSInputFile, URLInputFile,
    BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, CallbackData

from wbAPI import wbapi
from baseWB import work_db

# Создание отдельного роутера
router = Router()

# Словарь для запроса на внесение товара в БД
database_query_data = {
    'user_id': 0,
    'article': 0,
    'name': '',
    'starting_price': 0.0,
    'registration_date': '',
    'link_picture': '',
    'link_goods': ''
}


# Хендлер на регистрацию пользователя
@router.message(Command('start'))
async def any_message(message: Message):
    examination = await work_db.add_user(
        message.from_user.id, message.from_user.first_name
    )
    if examination:
        await message.answer(
            f'{message.from_user.first_name}, ваша учетная запись создана'
        )
    elif not examination:
        await message.answer(
            f'{message.from_user.first_name}, вы уже зарегистрированы'
        )
    else:
        await message.answer(
            f'{message.from_user.first_name}, что-то пошло не так!'
        )


# Хендлер на удаление пользователя
@router.message(Command('delete'))
async def any_message(message: Message):
    examination = await work_db.delete_user(message.from_user.id)
    if examination:
        await message.answer(
            f'{message.from_user.first_name}, ваша учетная запись и данные'
            ' успешно удалены'
        )
    elif not examination:
        await message.answer(
            f'{message.from_user.first_name}, вы еще не зарегистрированы'
        )
    else:
        await message.answer(
            f'{message.from_user.first_name}, что-то пошло не так!'
        )

# Хендлер для получения доп информации
@router.message(Command('info'))
async def any_message(message: Message):
    await message.answer(
        f'{message.from_user.first_name}, для внесения товара в Ваш список наблюдения необходимо '
        f'на странице товара скопировать ссылку и отправить её как сообщение боту, '
        f'так же можно в приложении поделиться ссылкой с ботом. После этого товар будет '
        f'внесен в БД для мониторинга цен.\nПри изменении цены Вам будет отправлено сообщении '
        f'об этом и информация по динамике цены, так же в сообщение будет содержаться ссылка на '
        f'товар для быстрого перехода на страницу товара.\nЕсли при мониторинге обнаружится что'
        f' статус товара на ВБ стал "нет в наличии", товар будет удален из БД бота'
    )


# Ответ на сообщение
@router.message(F.text)
async def extract_data(message: Message):
    # Проверка пользователя на регистрацию
    examination = await work_db.add_user(
        message.from_user.id, message.from_user.first_name
    )
    if examination:
        await message.answer(
            f'{message.from_user.first_name}, пройдите процедуру регистрации, нажмите кнопку меню'
            ' рядом с полем ввода сообщения и выберите команду <start>'
        )
    elif not examination:
        # Проверка правильности ввода ссылки
        article = wbapi.retrieving_article(message.text)
        if article is not None:
            data = await wbapi.get_current_price(article)
            msg = (
                f'{message.from_user.first_name}, товар: \n{data.get("name")},\n'
                f'с ценой {str(data.get("price"))} рублей,\nвнесен в Ваш список'
            )
            pic = await wbapi.get_pic_price(article)
            # Внесение данных в функцию занесения данных в БД
            # Проверка не 0-го состояния данных
            examination_goods = await work_db.add_goods_db(
                message.from_user.id,
                article,
                data.get('name'),
                data.get('price'),
                str(datetime.datetime.now()),
                pic,
                message.text,
            )
            print(examination_goods)
            if not examination_goods:
                await message.reply('Данный товар ранее уже внесен в список Ваших товаров')
            elif examination_goods:
                print(
                    message.from_user.first_name + ' внес товар:' + '\n' + data.get('name') + '\n' + 'по цене: '
                    + str(data.get('price')) + ' рублей'
                )
                await message.answer_photo(photo=pic, caption=msg)

            # database_query_data['user_id'] = message.from_user.id
            # database_query_data['article'] = article
            # database_query_data['name'] = data.get('name')
            # database_query_data['starting_price'] = data.get('price')
            # database_query_data['registration_date'] = str(datetime.datetime.now())
            # database_query_data['link_picture'] = pic
            # database_query_data['link_goods'] = message.text
            # Создание кнопки для внесения данных товара
            # builder = InlineKeyboardBuilder()
            # builder.row(InlineKeyboardButton(
            #     text='Нажмите для выбора товара',
            #     callback_data='check_record')
            # )
            # Отправка сообщения с информацией по товару и кнопкой
            # await message.answer_photo(photo=pic, caption=msg)
        else:
            await message.reply('Не корректно введена ссылка')
    else:
        await message.answer(
            f'{message.from_user.first_name}, что-то пошло не так!'
        )


# Обработка коллбеков
# Внесение товара в БД
@router.callback_query(F.data == "check_record")
async def send_random_value(callback: CallbackQuery):
    # Проверка не 0-го состояния данных
    if database_query_data['user_id'] == 0:
        print('Попали на 0')
        await callback.message.answer('Введите ссылку ещё раз')
    else:
        examination = await work_db.add_goods_db(
            database_query_data['user_id'],
            database_query_data['article'],
            database_query_data['name'],
            database_query_data['starting_price'],
            database_query_data['registration_date'],
            database_query_data['link_picture'],
            database_query_data['link_goods'])
        print(database_query_data)
        if not examination:
            await callback.message.answer('Данный товар ранее уже внесен в список Ваших товаров')
        elif examination:
            await callback.message.answer('Данный товар внесен в список Ваших товаров')
    # Обнуление данных товара
    database_query_data['user_id'] = 0
    database_query_data['article'] = 0
    database_query_data['name'] = ''
    database_query_data['starting_price'] = 0.0
    database_query_data['registration_date'] = ''
    database_query_data['link_picture'] = ''
    database_query_data['link_goods'] = ''

# # Хендлер Запрос по последним операциям
# @router.message(Command('requesttransac'))
# async def any_message(message: Message):
#     a = await tinApi.tin_get_last_transac()
#     for b in a[::-1]:
#         await message.answer(
#             ("""
# Вид операции: {}
# Название: {}
# Сумма операции: {} руб.
# Количество акций: {} шт.
# Дата: {}
# {}
#     """).format(b[4], b[0], b[5], b[2], b[3], b[1]),
#         )
#
#
# # Хендлер Информация по портфелю
# @router.message(Command("portf_inform"))
# async def any_message(message: Message):
#     await message.answer(
#         ('Всего денежек: ' +
#          str(tinApi.tin_portf()) + ' руб'),
#     )
# # @router.message()
# # async def any_message(message: Message):
# #     await message.send_message.SendMessage(
# #         chat_id=5369585473, text='str')
#
# # Проверка куня на содержание
# async def horse_check(*args):
#     # Читаем внуряшку из файла
#     try:
#         with open(args[0], "r") as read_file:
#             data = json.load(read_file)
#         flagLoading = data['flagLoading']
#         nameShare = data['name']
#         numLots = data['numLots']
#         lot = data['Lots']
#         timePur = data['timePur']
#         pricePur = data['pricePur']
#         a = """
# {} в {} заряжен акциями "{}" ценой {} руб, всего {} лотов при лотности {}
#                         """.format(args[1], timePur, nameShare,
#                                    pricePur, numLots, lot)
#         return a
#     except json.JSONDecodeError as e:
#         print("Ошибка при json 7 {}".format(args[0]))
# # Кунь первый проверка внутренностоей
# @router.message(Command("checking_first_horse"))
# async def any_message(message: Message):
#     await message.answer(await horse_check('horseArgs1.json',
#                                            'Кунь первый'
#                                            )
#                          )
# # Кунь второй проверка внутренностоей
# @router.message(Command("checking_second_horse"))
# async def any_message(message: Message):
#     await message.answer(await horse_check('horseArgs2.json',
#                                            'Кунь второй')
#                          )
# # Кунь третий проверка внутренностоей
# @router.message(Command("checking_third_horse"))
# async def any_message(message: Message):
#     await message.answer(await horse_check('horseArgs3.json',
#                                            'Кунь третий')
#                          )
# # Кунь четвертый проверка внутренностоей
# @router.message(Command("checking_fourth_horse"))
# async def any_message(message: Message):
#     await message.answer(await horse_check('horseArgs4.json',
#                                            'Кунь четвертый')
#                          )
#
# # Экстренная продажа куня
# async def emergency_sale_horse(*args):
#     # Читаем внуряшку из файла
#     try:
#         with open(args[0], "r") as read_file:
#             data = json.load(read_file)
#         flagLoading = data['flagLoading']
#         nameShare = data['name']
#         numLots = data['numLots']
#         lot = data['Lots']
#         timePur = data['timePur']
#         pricePur = data['pricePur']
#         ID = data['ID']
#         if flagLoading:
#             a = await tinApi.tin_sale_shares(int(numLots), ID)
#             if a != None:
#                 if a.execution_report_status != 1:
#                     return (args[1], ': Текущий статус заявки: неисполнена')
#                 else:
#                     print('Текущий статус заявки: исполнена')
#                 m1 = str(a.total_order_amount)
#                 m2 = str(a.executed_commission)
#                 #m3 = m1 * lot  # * selling.lots_executed
#                 a = """
# {} экстренно продан общей суммой {} руб, включая комиссию {} руб
#                     """.format(args[1], m2, m1)
#                 # Меняем значение флага
#                 data['flagLoading'] = bool(False)
#                 # Запмсываем данные
#                 try:
#                     with open(args[0], "w") as write_file:
#                         json.dump(data, write_file)
#                 except json.JSONDecodeError as e:
#                     print("Ошибка при json 7 {}".format(
#                         args[0]))
#             return a
#         else:
#             return ('Конь пустой')
#     except json.JSONDecodeError as e:
#         print("Ошибка при json 7 {}".format(args[0]))
# # Кунь первый экстренная продажа
# @router.message(Command("emergency_sale_first_horse"))
# async def any_message(message: Message):
#     await message.answer(await emergency_sale_horse('horseArgs1.json',
#                                            'Кунь первый'
#                                                     )
#                          )
# # Кунь второй экстренная продажа
# @router.message(Command("emergency_sale_second_horse"))
# async def any_message(message: Message):
#     await message.answer(await emergency_sale_horse('horseArgs2.json',
#                                            'Кунь второй'
#                                                     )
#                          )
# # Кунь третий экстренная продажа
# @router.message(Command("emergency_sale_third_horse"))
# async def any_message(message: Message):
#     await message.answer(await emergency_sale_horse('horseArgs3.json',
#                                            'Кунь второй'
#                                                     )
#                          )
# # Кунь четвертый экстренная продажа
# @router.message(Command("emergency_sale_fourth_horse"))
# async def any_message(message: Message):
#     await message.answer(await emergency_sale_horse('horseArgs4.json',
#                                            'Кунь четвертый'
#                                                     )
#                          )
#
# # Кунь первый запрос графика
# @router.message(Command("request_chart_first_horse"))
# async def any_message(message: Message):
#     a = graphicStory.line_graph('horseGraf1.json', 'horsePNG1.png')
#     if a == 'not':
#         await message.answer('Кунь первый график не построен - нет данных')
#     elif a == 'ok':
#         image = FSInputFile('horsePNG1.png')
#         await message.answer_photo(image, caption="График первого куня")
# # Кунь второй запрос графика
# @router.message(Command("request_chart_second_horse"))
# async def any_message(message: Message):
#     a = graphicStory.line_graph('horseGraf2.json', 'horsePNG2.png')
#     if a == 'not':
#         await message.answer('Кунь второй график не построен - нет данных')
#     elif a == 'ok':
#         image = FSInputFile('horsePNG2.png')
#         await message.answer_photo(image, caption="График второго куня")
# # Кунь третий запрос графика
# @router.message(Command("request_chart_third_horse"))
# async def any_message(message: Message):
#     a = graphicStory.line_graph('horseGraf3.json', 'horsePNG3.png')
#     if a == 'not':
#         await message.answer('Кунь третий график не построен - нет данных')
#     elif a == 'ok':
#         image = FSInputFile('horsePNG3.png')
#         await message.answer_photo(image, caption="График третего куня")
# # Кунь четвертый запрос графика
# @router.message(Command("request_chart_fourth_horse"))
# async def any_message(message: Message):
#     a = graphicStory.line_graph('horseGraf4.json', 'horsePNG4.png')
#     if a == 'not':
#         await message.answer('Кунь четвертый график не построен - нет данных')
#     elif a == 'ok':
#         image = FSInputFile('horsePNG4.png')
#         await message.answer_photo(image, caption="График четвертого куня")
# # Весь табун запрос графика
# @router.message(Command("request_chart_all_horse"))
# async def any_message(message: Message):
#     a = graphicStory.line_graph_all('horseGraf1.json', 'horseGraf2.json',
#                                 'horseGraf3.json', 'horseGraf4.json',
#                                 'horseAllPNG.png')
#     if a == 'not':
#         await message.answer('Табуна график не построен - нет данных')
#     elif a == 'ok':
#         image = FSInputFile('horseAllPNG.png')
#         await message.answer_photo(image, caption="График табуна")
