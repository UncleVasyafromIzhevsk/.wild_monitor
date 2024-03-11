# Выполняем запросы по артикулу(получаем в ссылке ТГ)
# https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm=
# после = ставим артикул

import asyncio
import httpx
import json
import datetime


# История цены по товару
# в историю попадают только последние изменения, текущая нет
async def product_price_history(*args):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(args[0])
            a = response.json()
            print(a)
            for r in a[::-1]:
                # print(a[0]['dt'])
                ts = r['dt']
                # print(a[0]['price']['RUB'])
                # Переводим в нормальное время
                value = datetime.datetime.fromtimestamp(ts)
                # print(value.strftime('%Y-%m-%d %H:%M:%S'))
                # Переводим цены в рубли
                price = (r['price']['RUB']) // 100
                # print(price)
                print('На дату {} цена была {} рублей'.format(value, price))
        except json.JSONDecodeError as e:
            print('Ошибка при обработке json история цены')
# asyncio.run(product_price_history('https://basket-10.wbbasket.ru/vol1375/part137593/137593603/info/price-history.json'))

# Получение текущей цены товара, цены обманки и состояния наличия товара
# В аргумент передаем артикул
async def get_current_price(*args):
    baseURL = ('https://card.wb.ru/cards/v1/detail?appType=' +
               '1&curr=rub&dest=-1257786&spp=30&nm=')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(baseURL + args[0])
            a = response.json()
            issue_price = (a['data']['products'][0])['priceU']
            true_price = (a['data']['products'][0])['salePriceU']
            b = (((a['data']['products'][0])['sizes'])[0])['stocks']
            if not b:
                is_available = False
            else:
                is_available = True
            print("""
Цена обманка {} руб
Цена истина {} руб
В наличии: {}    
            """.format(
                    issue_price // 100, true_price // 100,
                    is_available
                ))
        except Exception as e:
            print(e)
#asyncio.run(get_current_price('204572079'))
