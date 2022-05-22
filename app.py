import requests

import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui

import design


API = '803fc8345147cba4b9c0497a02566199'


def get_weather(city):  # sourcery skip: avoid-builtin-shadow
    city_id = 0
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city.lower(), 'type': 'like', 'units': 'metric', 'APPID': API})
        data = res.json()
        cities = [f"{d['name']} ({d['sys']['country']})" for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
        return 'Ошибка! Такого города/штата/региона/страны не найдено'
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric',
                                   'lang': 'ru', 'APPID': API})
        data = res.json()
        # http://openweathermap.org/img/wn/10d@2x.png
        icon = requests.get("http://openweathermap.org/img/wn/"
                            f"{data['weather'][0]['icon']}@2x.png")
        with open('weather_image.png', 'wb') as file:
            file.write(icon.content)
        type = ''
        data_type = data['sys'].get('type')
        if data_type == 1:
            type = 'городе'
        elif data_type == 2:
            type = 'регионе/штате'
        app.setWindowIcon(QtGui.QIcon('./weather_image.png'))
        window.setWindowTitle(f"Погода в {type} \"{data['name']}\"")
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])
        return (
            f"В {type} \"{data['name']}\" [{cities[0]}]\n"
            f"Сейчас {data['weather'][0]['description']}\n"
            f"Температура: {data['main']['temp']}"
        )
    except Exception as e:
        print("Exception (weather):", e)
        return 'Ошибка! Погода не найдена'


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.get_data)

    def get_data(self):
        city = self.lineEdit.text().strip().lower()
        print(city)
        self.label.setText(get_weather(city))


def main():
    global app
    global window
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.setWindowTitle('Погода')

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == "__main__":
    main()
