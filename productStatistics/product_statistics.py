# Модуль будет составлять график изменения цены, печатать его в изображение
# а так же рассчитывать разницу между начальной ценой (ценой при внесение товара) и
# новой ценной, полученной по API

import matplotlib.pyplot as plt


def bar_graph(**kwargs):
    data_time = kwargs['data']
    price = kwargs['price']
    name = kwargs['name']
    percent = percent_change(starting_price=price[0], last_price=price[len(price) - 1])
    try:
        # Стиль
        plt.style.use('fivethirtyeight')
        # plot
        fig, ax = plt.subplots()
        # Убрать наименования оси x
        ax.get_xaxis().set_visible(False)
        # сетка, в данном случае убрали ее
        plt.grid(False)
        # График
        bars = ax.barh(data_time, price, color='green')
        # Надписи значений прямо на столбцах
        ax.bar_label(
            bars, padding=-45, color='orange', fontsize=10, label_type='edge', fontweight='bold',
            fontstyle='oblique'
        )
        # Масштабирование столбцов(надо доделать)
        a = price[0] // 10
        ax.set(xlim=(price[0] - a, price[len(price) - 1] + a))
        # Поворот надписей на оси и их параметры
        plt.yticks(rotation=70, fontsize='xx-small', fontstyle='oblique')
        # Текст на графике
        plt.text(
            price[len(price) - 1], data_time[0], ('Цена\nизменилась\nна: ' + percent),
            color='red', fontsize=15, fontweight='bold', fontstyle='oblique'
        )
        # Линия как-бы ограничительная(настроить значение на первоначальную цену)
        ax.axvline(x=price[0], zorder=0, color='blue', ls='-', lw=1)
        # Цвет фона
        # ax.set_facecolor("yellow")
        # наименование
        plt.title(name)
        # plt.xlabel('Дата и время')
        # plt.ylabel('Цена, руб')
        # Убрать окошко осей
        plt.box(False)
        # Показать
        plt.show()
        # записать в картинку
        # plt.savefig('test.png')
    except Exception as e:
        print(
            f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}, 'При построении графика'")


# Декаратор для отправки строки с процентом
def percent_str(func):
    try:
        def wrapper(**kwargs):
            percent = int(func(**kwargs))
            if percent >= 0:
                out_str = f'+{str(percent)} %'
            else:
                out_str = f'{str(percent)} %'
            return out_str
        return wrapper
    except Exception as e:
        print(
            f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}, 'При преобразовании % в str'")


# Получение изменения в процентах между начальной и последней ценой
@percent_str
def percent_change(**kwargs):
    try:
        starting_price = kwargs['starting_price']
        last_price = kwargs['last_price']
        percent = (1 - (last_price / starting_price)) * 100
        return percent
    except Exception as e:
        print(
            f"Тип исключения: {type(e).__name__}, сообщение: {str(e)}, 'При расчете процента'")


# bar_graph(data=['2024-04-05 20:58', '2024-04-11 20:11', '2024-04-13 20:11'],
#           price=[101, 102, 130], name='black coffe')
# percent_change(starting_price=11, last_price=13)
