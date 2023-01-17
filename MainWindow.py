import copy
import random
from tkinter import messagebox
from Graph import *
from SolutionWindow import *
import math


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.__graph = Graph()              # створюємо об'єкт графу, щоб взаємодіяти в меню з ним
        self.__matrix = None                # матриця для збереження даних, що вводить користувач
        self.__floyd_IsEnabled = False      # перевірка кнопки активації методу Флойда
        self.__dantzig_IsEnabled = False    # перевірка кнопки активації методу Данцига
        self.__confirm_IsEnabled = False    # перевірка кнопки підтвердження

        # БАЗОВІ ПАРАМЕТРИ ІНТЕРФЕЙСУ
        self.label_font = ("Mazzard Soft L", 12, 'bold')
        self.button_font = ("Mazzard Soft M", 8, 'normal')
        self.main_color = '#6c7575'
        self.button_color = '#a5d9d5'
        self.label_color = 'black'

        self.title("Main window")
        self.geometry("375x400+448+240")
        self.resizable(False, False)

        # ПРОСТІР ОСНОВНОГО ВІКНА
        self.frame = Frame(self, bg=self.main_color)
        self.frame.place(x=0, y=0, width=375, height=400)

        # ПРОСТІР ДЛЯ КНОПОК ВИБОРУ АЛГОРИТМА
        self.frame_method = Frame(self.frame, bg=self.main_color, relief='raised', bd=1)
        self.frame_method.place(x=0, y=340, width=250, height=60)

        self.label_choose = Label(self.frame_method, text='Обери алгоритм: ', font=self.label_font, bg=self.main_color,
                                  anchor='n')
        self.label_choose.pack()

        self.button_dantzig = Button(self.frame_method, text='Метод Данцига', font=self.button_font,
                                     bg=self.button_color, command=self.button_dantzig_method_click)
        self.button_dantzig.place(relx=0.12, rely=0.425)

        self.button_floyd = Button(self.frame_method, text='Метод Флойда', font=self.button_font, bg=self.button_color,
                                   command=self.button_floyd_method_click)
        self.button_floyd.place(relx=0.5, rely=0.425)

        # ПРОСТІР ДЛЯ КНОПОК РОБОТИ З МАТРИЦЕЮ
        self.frame_matrix_space = Frame(self.frame, bg=self.main_color, relief='raised')
        self.frame_matrix_space.place(x=0, y=0, width=375, height=340)

        self.label_matrix_size = Label(self.frame_matrix_space, text='Розмір матриці: ', font=self.label_font,
                                       bg=self.main_color)
        self.label_matrix_size.place(relx=0.05, rely=0.04)

        self.entry_matrix_size = Entry(self.frame_matrix_space, width=2, font=self.label_font)
        self.entry_matrix_size.place(relx=0.4, rely=0.04)

        self.button_create_matrix = Button(self.frame_matrix_space, text='Створити матрицю', font=self.button_font,
                                           bg=self.button_color, command=self.button_create_matrix_click)
        self.button_create_matrix.place(relx=0.475, rely=0.04, relwidth=0.275)

        self.button_confirm_matrix = Button(self.frame_matrix_space, text='Підтвердити', font=self.button_font,
                                            bg=self.button_color, height=1,
                                            command=self.button_confirm_matrix_click)
        self.button_confirm_matrix.place(relx=0.765, rely=0.04, relwidth=0.185)

        self.button_autofill = Button(self.frame_matrix_space, text='Автозаповнення', font=self.button_font,
                                      bg=self.button_color, height=1, command=self.button_autofill_click)
        self.button_autofill.place(relx=0.05, rely=0.9, relwidth=0.25)

        self.button_clear_matrix = Button(self.frame_matrix_space, text='Очистити', font=self.button_font,
                                          bg=self.button_color, height=1, command=self.button_clear_matrix_click)
        self.button_clear_matrix.place(relx=0.75, rely=0.9, relwidth=0.2)

        # ПРОСТІР ДЛЯ МАТРИЦІ
        self.frame_matrix = Frame(self.frame_matrix_space, bg=self.main_color, relief='ridge', bd=1)
        self.frame_matrix.place(relx=0.05, rely=0.14, height=250, relwidth=0.9)

        # КНОПКА ОТРИМАННЯ РЕЗУЛЬТАТУ
        self.button_get_result = Button(self.frame, text='Отримати результат', font=self.button_font, bg=self.button_color,
                                command=self.button_get_result_click)
        self.button_get_result.place(x=250, y=340, height=60, width=125)

    @property
    def graph(self):
        return self.__graph

    @graph.setter
    def graph(self, graph):
        self.__graph = graph

    @property
    def matrix(self):
        return self.__matrix

    @matrix.setter
    def matrix(self, matrix):
        self.__matrix = matrix


    # КНОПКА ДЛЯ ОТРИМАННЯ РЕЗУЛЬТАТУ ТА ЙОГО ВИВЕДЕННЯ
    def button_get_result_click(self):
        if self.__confirm_IsEnabled == False:
            messagebox.showwarning(title='Попередження', message='Підтвердіть створену матрицю')
            return
        self.__graph.drawGraph()
        if self.__floyd_IsEnabled == True:
            try:
                self.__graph.floydMethod()
            except:
                messagebox.showwarning(title='Попередження', message='Знайдений негативний контур. Введіть нову матрицю')
                return
        elif self.__dantzig_IsEnabled == True:
            try:
                self.__graph.dantzigMethod()
            except:
                messagebox.showwarning(title='Попередження', message='Знайдений негативний контур. Введіть нову матрицю')
                return
        else:
            messagebox.showwarning(title="Попередження", message="Оберіть метод розв'язання")
            return

        solution_window = SolutionWindow()
        with open("data.txt", 'r', encoding='utf-8') as file:
            text = file.read()
        solution_window.text_result.insert(1.0, text)
        solution_window.mainloop(1)

        self.__floyd_IsEnabled = False
        self.__dantzig_IsEnabled = False
        self.__confirm_IsEnabled = False

    # СТВОРЕННЯ ПРОСТОРУ ДЛЯ МАТРИЦІ
    def button_create_matrix_click(self):
        size = self.entry_matrix_size.get()
        if not size.isdigit() or int(size) < 1 or int(size) > 15:
            messagebox.showwarning(title="Попередження", message="Введіть коректний розмір (1-15) ")
            self.entry_matrix_size.delete(0, END)
            return

        self.__graph.size = int(size)
        self.__matrix = [[None for x in range(self.__graph.size)] for y in range(self.__graph.size)]

        for i in range(self.__graph.size):
            for j in range(self.__graph.size):
                entry = Entry(self.frame_matrix, bg='white', font=50, justify='center')
                entry.place(relx=j / self.__graph.size, rely=i / self.__graph.size, relwidth=1 / self.__graph.size,
                            relheight=1 / self.__graph.size)
                self.__matrix[i][j] = entry
        self.__confirm_IsEnabled = False

    # ПІДТВЕРДЖЕННЯ СТВОРЕНОЇ МАТРИЦІ ТА ВАЛІДАЦІЯ ДАНИХ
    def button_confirm_matrix_click(self):
        if self.__matrix == None:
            messagebox.showwarning(title='Попередження', message='Спочатку створіть матрицю')
            return

        self.__graph.matrix = [[None for x in range(self.__graph.size)] for y in range(self.__graph.size)]
        for i in range(self.__graph.size):
            for j in range(self.__graph.size):
                element = self.__matrix[i][j].get()
                if i == j:
                    if element != '0':
                        messagebox.showwarning(title='Попередження',
                                               message='Основна діагональ може складатися лише з 0')
                        return 0
                    else:
                        self.__graph.matrix[i][j] = int(element)
                else:
                    if element == 'Inf' or element == 'inf':
                        self.__graph.matrix[i][j] = math.inf
                    elif element != '' and element[0] == '-' and element[1:].isdigit():
                        self.__graph.matrix[i][j] = int(element)
                    elif element == '' or not element.isdigit():
                        messagebox.showwarning(title='Попередження', message="Введіть коректні значення (Inf або ціле число)")
                        return
                    else:
                        self.__graph.matrix[i][j] = int(element)
        messagebox.showinfo(title='Інфо', message='Матриця успішно створена')
        self.__confirm_IsEnabled = True

    # АВТОЗАПОВНЕННЯ ВИПАДКОВИМИ ЗНАЧЕННЯМИ
    def button_autofill_click(self):
        if self.__matrix == None:
            messagebox.showwarning(title='Попередження', message='Спочатку створіть матрицю')
            return

        list_elements = [x for x in range(1, 10)]

        for j in range(0, self.__graph.size):
            for i in range(j, self.__graph.size):
                random_value = []
                entry = self.__matrix[i][j]
                entry.delete(0, END)
                if i == j:
                    entry.insert(0, 0)
                else:
                    random_value.append(random.choice(list_elements))
                    random_value.append('Inf')
                    entry.insert(0, random.choice(random_value))
                    entry = self.__matrix[j][i]
                    entry.delete(0, END)
                    entry.insert(0, random.choice(random_value))

    # ОЧИСТКА ВСІХ УВЕДЕНИХ ДАННИХ
    def button_clear_matrix_click(self):
        self.entry_matrix_size.delete(0, END)

        self.__matrix = None
        self.__confirm_IsEnabled = False

        self.frame_matrix.destroy()
        self.frame_matrix = Frame(self.frame_matrix_space, bg=self.main_color, relief='ridge', borderwidth=1)
        self.frame_matrix.place(relx=0.05, rely=0.14, height=250, relwidth=0.9)

    # ПЕРЕМИКАЧ КНОПОК АКТИВАЦІЇ МЕТОДІВ
    def button_dantzig_method_click(self):
        self.__floyd_IsEnabled = False
        self.__dantzig_IsEnabled = True
        return

    # ПЕРЕМИКАЧ КНОПОК АКТИВАЦІЇ МЕТОДІВ
    def button_floyd_method_click(self):
        self.__floyd_IsEnabled = True
        self.__dantzig_IsEnabled = False
        return
