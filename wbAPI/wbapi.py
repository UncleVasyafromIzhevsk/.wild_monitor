# Выполняем запросы по артикулу(получаем в
# ссылке ТГ)
# https://card.wb.ru/cards/v1/detail?appType=
# 1&curr=rub&dest=-1257786&spp=30&nm=
# после = ставим артикул

import asyncio
import httpx


# Вайлдберрис
# Извлечение артикула
def retrieving_article(*args):
    try:
        print(args[0])
        idx = args[0].find('https://')
        article_comp = args[0][idx:len(args[0])]
        print(article_comp)
        if args[0].find("wildberries.ru/catalog/") != -1:
            article = article_comp.split('/')
            print(article[4])
            return article[4]
        else:
            return None
    except Exception as e:
        print(f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}")


# retrieving_article('ThinkPad L460 i3 8/128/6generation lenovohttps://wildberries.ru/catalog/
# 179968448
#     /detail.aspx')

# Получение текущей цены товара, названия и состояния наличия товара
# В аргумент передаем артикул
async def get_current_price(*args):
    baseURL = ('https://card.wb.ru/cards/v1/detail?appType=' +
               '1&curr=rub&dest=-1257786&spp=30&nm=')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(baseURL + args[0])
            a = response.json()
            name = (a['data']['products'][0])['name']
            true_price = ((a['data']['products'][0])['salePriceU']) / 100
            b = (((a['data']['products'][0])['sizes'])[0])['stocks']
            if not b:
                is_available = False
            else:
                is_available = True
            c = {'name': name, 'price': true_price, 'is_available': is_available, 'getURL': (baseURL + args[0])}
            # print(c)
            return c
        except Exception as e:
            print(e)
            return False
# asyncio.run(get_current_price('204572079'))

# Извлечение URL изображение товара
async def get_pic_price(*args):
    # Перебираем корзины от 0 до 15
    for idx in range(0, 16):
        try:
            # Если артикул 9-и значный то адрес
            if len(args[0]) == 9:
                if idx < 10:
                    basket = '0' + str(idx)
                elif idx >= 10:
                    basket = idx
                picURL = ('https://basket-{}.wbbasket.ru/'.format(basket) +
                          'vol{}/part{}/{}/images/big/1.webp'.format(args[0][:4], args[0][:6], args[0]))
            # Если артикул 8-и значный то адрес
            elif len(args[0]) == 8:
                if idx < 10:
                    basket = '0' + str(idx)
                elif idx >= 10:
                    basket = idx
                picURL = ('https://basket-{}.wbbasket.ru/'.format(basket) +
                          'vol{}/part{}/{}/images/big/1.webp'.format(args[0][:3], args[0][:5], args[0]))
            print(picURL)
            async with httpx.AsyncClient() as client:
                response = await client.get(picURL)
                print(response.status_code)
                if response.status_code == 200:
                    return picURL
        except Exception as e:
            print(f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}")
# asyncio.run(get_pic_price('70520736'))
