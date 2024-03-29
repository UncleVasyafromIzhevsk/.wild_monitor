import json
import re


from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (Message, ReplyKeyboardRemove, FSInputFile,
                           URLInputFile, BufferedInputFile)


from wbAPI import wbapi

# Создание отдельного роутера
router = Router()

# Хендлер на регистрацию пользователя
@router.message(Command('start'))
async def any_message(message: Message):
    print(message.from_user.id, message.from_user.first_name)
    await message.answer('Будет рега')

# Ответ на сообщение
@router.message(F.text)
async def extract_data(message: Message):
    article = wbapi.retrieving_article(message.text)
    if article != None:
        data = await wbapi.get_current_price(article)
        pic = await wbapi.get_pic_price(article)
        await message.reply_photo(photo=pic, caption=data)
    else:
        await message.reply('Не корректно введена ссылка')



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




