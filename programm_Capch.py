import sqlite3
import sys
import os

from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from designe_capcha_END import Ui_MainWindow
from random import choice
from PyQt5.QtCore import Qt


# объявляем классы ошибок
# если не выбран алфавит
class NotAlphabet(Exception):
    pass


# если сказано неверное количество или текст
class WrongNum(Exception):
    pass


# если не выбран вид изменений картинки
class NotSpoil(Exception):
    pass


# главный класс
class Main_Widget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
         
    def initUI(self):
        # название проекта
        self.setWindowTitle("Captcha Generator") 
        # переменные для определения нажатой кнопки
        self.power = 0
        self.sign = 0
        self.spoil = 0
        self.B_or_s = -1           
        # подключаем базу данных
        self.connection = sqlite3.connect("Captchas_BD")    
        self.cursor = self.connection.cursor()
        # инициализируем объекты(задаём текст, цвет)   
        self.pushButtonC.setStyleSheet("background-color: white;")
        self.lineEdit_quantity.clear()
        self.BtnBackToCust.setStyleSheet("background-color: '#7b917b';")
        self.BtnCleanBd.setStyleSheet("background-color: '#7b917b';")
        
        self.label.setText('Мощность алфавита:')
        self.BtnBackToCust.setText('вернуться к настройкам')
        self.radioBtn1.setText('Русский + цифры')
        self.radioBtn2.setText('Англиский + цифры')
        self.radioBtn3.setText('Только цифры')
        self.pushButtonC.setText('ПРОВЕРИТЬ')
        self.label_spoil.setText('Вид капчи:')
        self.radioBtn4.setText('Линия')
        self.radioBtn5.setText('Наклон букв')
        self.radioBtn6.setText('Оба варианта')
        self.radioBtn_BL.setText('Заглавные буквы')
        self.BtnCleanBd.setText('очистить базу данных')
        self.label_quantity.setText('Введите количесво \n(не больше 10)')
        # подключаем кнопки к нужным функциям
        # кнопки для выбора алфавита
        self.radioBtn1.clicked.connect(self.choice1_alphabet)
        self.radioBtn2.clicked.connect(self.choice2_alphabet)
        self.radioBtn3.clicked.connect(self.choice3_alphabet)
        # кнопки проверки, запуска, возвращения к настройкам, очистки базы данных
        self.pushButtonC.clicked.connect(self.Check)
        self.pushButtonG.clicked.connect(self.GENERATE_DIRECTORY)
        self.BtnBackToCust.clicked.connect(self.PREPARATIONS_TO_GENERATE)
        self.BtnCleanBd.clicked.connect(self.CLEAN_BD)
        # кнопки для выбора изменений в изображении
        self.radioBtn4.clicked.connect(self.choice1_spoil)
        self.radioBtn5.clicked.connect(self.choice2_spoil)
        self.radioBtn6.clicked.connect(self.choice3_spoil)
        self.radioBtn_BL.clicked.connect(self.Big_or_small)
        # прячем ненужные на данный момент кнопки
        self.pushButtonC.show()
        self.BtnBackToCust.hide()
        self.pushButtonG.hide()
        self.BtnCleanBd.hide()
        
    # закрываем окно при нажатии на Esc   
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            sys.exit(app.exec())   
    # функции нужные чтобы понять какая кнопка нажата
    # функции отвечающие за алфавит
    
    def choice1_alphabet(self):
        self.power = 1
        
    def choice2_alphabet(self):
        self.power = 2

    def choice3_alphabet(self):
        self.power = 3
        
    # функции отвечающие за вид капчи  
    def choice1_spoil(self):
        self.spoil = 1
    
    def choice2_spoil(self):
        self.spoil = 2
    
    def choice3_spoil(self):
        self.spoil = 3
        
    # функция отвечающая за заглавные буквы    
    def Big_or_small(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.B_or_s = 1
        else:
            self.B_or_s = -1
            
    # проверка на корректность введённых данных   
    def Check(self):
        # возвращаем надписи в нормальное состояние
        # self.ind это индикатор ошибок если их нет то он равен 0
        self.ind = 0
        self.label.setText('Мощность алфавита:')
        self.label_quantity.setText('Введите количесво \n(не больше 10)')
        self.label_spoil.setText('Вид капчи:')
        # блоки try except
        try:
            # провека алфавита
            if self.power == 0:
                raise NotAlphabet()
        
        except NotAlphabet:
            # в случае ошибки меняем текст и цвет кнопки 
            self.pushButtonC.setText('ПРОВАЛ')
            self.label.setText('Укажите мощность:')
            self.pushButtonC.setStyleSheet("background-color: red;")
            # есть ошибка значит self.ind = 1
            self.ind = 1
            
        try:
            # проверка вида капчи
            if self.spoil == 0:
                raise NotSpoil()    
            
        except NotSpoil:
            # в случае ошибки меняем текст и цвет кнопки 
            self.pushButtonC.setText('ПРОВАЛ')
            self.pushButtonC.setStyleSheet("background-color: red;")
            self.label_spoil.setText('Вы не указали \n вид')
            # есть ошибка значит self.ind = 1
            self.ind = 1
            
        try:  
            # проверка на то что количесто капч не строка и лежит в нужном диапазоне
            if (int(self.lineEdit_quantity.text()) <= 0)or(int(self.lineEdit_quantity.text()) >= 11):
                raise WrongNum()   
        # если введена строка    
        except ValueError:
            # в случае ошибки меняем текст и цвет кнопки 
            self.pushButtonC.setText('ПРОВАЛ')
            self.pushButtonC.setStyleSheet("background-color: red;")
            self.label_quantity.setText('ЗНАЧЕНИЕ ДОЛЖНО \nБЫТЬ ЧИСЛОМ')
            # есть ошибка значит self.ind = 1
            self.ind = 1
        # если число не лежит в нужном диапазоне        
        except WrongNum:
            # в случае ошибки меняем текст и цвет кнопки 
            self.pushButtonC.setText('ПРОВАЛ')
            self.pushButtonC.setStyleSheet("background-color: red;")
            self.label_quantity.setText('НЕВЕРНОЕ ЗНАЧЕНИЕ')    
            # есть ошибка значит self.ind = 1
            self.ind = 1
        # если ошибок нет и self.ind = 0 то приступим к генерации
        if self.ind == 0:
            # прячем лишнее
            self.HIDE_USELESS()
            self.pushButtonC.hide()
            # показываем скрытые кнопки
            self.BtnCleanBd.show()
            self.BtnBackToCust.show()
            self.pushButtonG.show()
            # меняем цвет
            self.pushButtonG.setStyleSheet("background-color: green;")
            self.pushButtonG.setText('СГЕНЕРИРОВАТЬ!')
            
    # создаём дирректорию для хранения файлов с капчами                
    def GENERATE_DIRECTORY(self):
        # указываем путь
        self.way = "Result_Capcha/"
        # 1 часть имени файла
        name = 'Captchas'
        # 2 часть имени файла
        num = 0 
        # создаём уникальное имя файла вида: 'Captchas' + число
        while True:
            try:
                self.file_name = name + '_' + str(num)
                self.result = self.way + name + '_' + str(num)
                os.mkdir(self.result)
            except OSError:
                # если возникла ошибка то увеличиваем 'число'
                num += 1
            else:
                break   
        # вызываем функцию генерации текста    
        self.GENERATE_TEXT()
        
    # функция кторая прячет лишнее        
    def HIDE_USELESS(self):
        self.radioBtn1.hide()
        self.radioBtn2.hide()
        self.radioBtn3.hide()
        self.radioBtn4.hide()
        self.radioBtn5.hide()
        self.radioBtn6.hide()
        self.radioBtn_BL.hide()
        
        self.label_spoil.hide()
        self.label.hide()
        self.label_quantity.hide()
        self.lineEdit_quantity.hide()
        
    # функция которая показывает нужное   
    def SHOW_USEFUL(self):
        self.radioBtn1.show()
        self.radioBtn2.show()
        self.radioBtn3.show()
        self.radioBtn4.show()
        self.radioBtn5.show()
        self.radioBtn6.show()
        self.radioBtn_BL.show()
        
        self.label_spoil.show()
        self.label.show()
        self.label_quantity.show()
        self.lineEdit_quantity.show()
        
    # функция которая "чистит" базу данных  
    def CLEAN_BD(self):     
        self.cursor.execute('DROP TABLE IF EXISTS info')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS info(
                        id INTEGER PRIMARY KEY, name TEXT, 
                        color TEXT,  spoil TEXT,
                        file_way TEXT
                        )''')     
        
    # собственно та самая функция генерации текста
    def GENERATE_TEXT(self):  
        # выбираем алфавит
        if self.power == 1:
            self.Symrange = Russian + Numbers
        elif self.power == 2:
            self.Symrange = English + Numbers
        else:
            self.Symrange = Numbers
        # необходимое количесто капч    
        self.Quantity = int(self.lineEdit_quantity.text())
        
        for i in range(self.Quantity):
            self.capcha_text = ''
            for j in range(6):
                if self.B_or_s == 1:
                    # рандомно выбираем размер(если пользователь нажал на кнопку) и символ
                    RandomSize = choice((lambda x: x.upper(), lambda x: x.lower()))
                    self.capcha_text += RandomSize(choice(self.Symrange))
                else:
                    self.capcha_text += choice(self.Symrange)
            # функция создающая изображение      
            self.GENERATE_IMAGE(self.capcha_text)   
            
    # функция подготавливающая программу к новой генерации        
    def PREPARATIONS_TO_GENERATE(self):
        self.pushButtonC.show()
        self.BtnBackToCust.hide()
        self.BtnCleanBd.hide()
        self.pushButtonG.hide()
        self.pushButtonC.setText('ПРОВЕРИТЬ')
        self.pushButtonC.setStyleSheet("background-color: white;")
        self.SHOW_USEFUL()
        
    # создаём изображение         
    def GENERATE_IMAGE(self, text):
        # случайным образом выбираем фон капчи 
        capcha_name = (choice(('Background1.jpg', 'Background2.jpg',
                               'Background3.jpg', 'Background4.jpg',
                               'Background5.jpg', 'Simple_Background.jpg')))
        self.capcha = Image.open(capcha_name)
        # в зависимости от фона выбираем цвет(чтобы не ломать глаза)
        if capcha_name == 'Background3.jpg':
            self.capcha_color = '#ff0000'
        elif capcha_name == 'Background5.jpg':
            self.capcha_color = '#ffffff'
        elif capcha_name == 'Simple_Background.jpg':
            self.capcha_color = '#7b917b'            
        elif capcha_name == 'Background2.jpg':
            self.capcha_color = '#ffff00' 
        else:
            self.capcha_color = '#000000'
        # выбираем шрифт   
        self.font = ImageFont.truetype("FreeMono.ttf", 50, encoding="unic")
        # наносим текст на изображение
        self.draw_capcha = ImageDraw.Draw(self.capcha)
        self.draw_capcha.text((12, 25), text, font=self.font, fill=(self.capcha_color))
        # в зависимости от нажатой кнопки выбираем соответствующее изменение
        if self.spoil == 1:
            self.GENERATE_IMAGE_LINE(text)
        elif self.spoil == 2:
            self.GENERATE_IMAGE_OVERTURN(text)
        else:
            # если нажата кнопка "Всё вместе" то мы рандомно выбираем из 2 вариантов изменений
            RandomSpoil = choice((1, 0))
            if RandomSpoil == 1:
                self.GENERATE_IMAGE_LINE(text)
            else:
                self.GENERATE_IMAGE_OVERTURN(text)   
                
    # рисуем линию    
    def GENERATE_IMAGE_LINE(self, text):
        self.draw_capcha.line((11, 55, 190, 55), fill=(self.capcha_color), width=2)
        # а это для базы данных
        self.viev = 'line'
        self.color = self.capcha_color 
        # сохраняем результат
        self.SAVE_AS(self.capcha, text)
        
    # поворачиваем буквы    
    def GENERATE_IMAGE_OVERTURN(self, text): 
        # создаём изображения нужного размера(учитывая шрифт)
        Letter1 = Image.new('L', ((self.font.getsize(text[0]))[0], sum(self.font.getmetrics())))
        Letter2 = Image.new('L', ((self.font.getsize(text[1]))[0], sum(self.font.getmetrics())))
        Letter3 = Image.new('L', ((self.font.getsize(text[2]))[0], sum(self.font.getmetrics())))
        Letter4 = Image.new('L', ((self.font.getsize(text[3]))[0], sum(self.font.getmetrics())))
        Letter5 = Image.new('L', ((self.font.getsize(text[4]))[0], sum(self.font.getmetrics())))
        Letter6 = Image.new('L', ((self.font.getsize(text[5]))[0], sum(self.font.getmetrics())))
        # мы будем рисовать каждый символ отвельно(чтобы наклонять изображение)
        draw_letter1 = ImageDraw.Draw(Letter1)
        draw_letter2 = ImageDraw.Draw(Letter2)
        draw_letter3 = ImageDraw.Draw(Letter3)
        draw_letter4 = ImageDraw.Draw(Letter4)
        draw_letter5 = ImageDraw.Draw(Letter5)
        draw_letter6 = ImageDraw.Draw(Letter6)
        # рисуем
        draw_letter1.text((0, 0), text[0], font=self.font, fill=('#FFFFFF'))
        draw_letter2.text((0, 0), text[1], font=self.font, fill=('#FFFFFF'))
        draw_letter3.text((0, 0), text[2], font=self.font, fill=('#FFFFFF'))
        draw_letter4.text((0, 0), text[3], font=self.font, fill=('#FFFFFF'))
        draw_letter5.text((0, 0), text[4], font=self.font, fill=('#FFFFFF'))
        draw_letter6.text((0, 0), text[5], font=self.font, fill=('#FFFFFF'))
        # теперь поворачиваем
        Letter2 = Letter2.rotate(15, resample=Image.BICUBIC, expand=True)
        Letter3 = Letter3.rotate(20, resample=Image.BICUBIC, expand=True)
        Letter5 = Letter5.rotate(345, resample=Image.BICUBIC, expand=True)
        Letter6 = Letter6.rotate(330, resample=Image.BICUBIC, expand=True)
        # да да, ещё раз
        capcha_name_new = (choice(('Background1.jpg', 'Background2.jpg',
                                   'Background3.jpg', 'Background4.jpg',
                                   'Background5.jpg', 'Simple_Background.jpg')))
        capcha = Image.open(capcha_name_new)
        if capcha_name_new == 'Background3.jpg':
            capcha_color = '#ff0000'
        elif capcha_name_new == 'Background5.jpg':
            capcha_color = '#ffffff'
        elif capcha_name_new == 'Simple_Background.jpg':
            capcha_color = '#7b917b'            
        elif capcha_name_new == 'Background2.jpg':
            capcha_color = '#ffff00'  
        else:
            capcha_color = '#000000' 
        # накладывем наклонённые буквы на итоговое изображение
        capcha.paste(capcha_color, box=(10, 10), mask=Letter1) 
        capcha.paste(capcha_color, box=(30, 12), mask=Letter2)
        capcha.paste(capcha_color, box=(60, 18), mask=Letter3)
        capcha.paste(capcha_color, box=(95, 30), mask=Letter4)
        capcha.paste(capcha_color, box=(120, 18), mask=Letter5)
        capcha.paste(capcha_color, box=(150, 12), mask=Letter6)
        # это надо для базы данных   
        self.viev = 'slant'
        self.color = capcha_color
        # сохраняем результат
        self.SAVE_AS(capcha, text)
        
    def SAVE_AS(self, capcha, text): 
        # сохранение......
        self.file_way = self.result + '/' + text + '.jpg'
        capcha.save(self.result + '/' + text + '.jpg')
        # теперь надо заполнить базу данных
        self.DATABASE()
        
    def DATABASE(self):
        # это то что мы будем записывать
        V1n = "'" + self.capcha_text + "'"
        V2c = "'" + self.color + "'"
        V3s = "'" + self.viev + "'"
        V4fw = "'" + self.file_way + "'"
        # создаём строку/команду
        add_values = "INSERT INTO info(name, color, spoil, file_way) VALUES \
            (" + V1n + "," + V2c + "," + V3s + "," + V4fw + ");"
        # записываем
        self.cursor.execute(add_values)
        self.connection.commit()

   
# алфавиты:            
Russian = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
           'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
           'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
English = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z']
Numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Widget()
    ex.show()
    sys.exit(app.exec())
    
    