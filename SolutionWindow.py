from tkinter import *

from PIL import Image, ImageTk

class SolutionWindow(Toplevel):
    def __init__(self):
        super().__init__()

        self.label_font = ("Mazzard Soft L", 12, 'bold')
        self.button_font = ("Mazzard Soft M", 8, 'normal')
        self.main_color = '#6c7575'
        self.button_color = '#a5d9d5'
        self.label_color = 'black'

        self.title("Solution")
        self.geometry("1020x570+850+175")
        self.resizable(False, False)

        self.frame_solution = Frame(self, bg=self.main_color)
        self.frame_solution.place(x=0, y=0, width=1020, height=570)

        # ІМПОРТ ФОТО ГРАФУ З ПК
        self.image = Image.open("graph.png")
        photo = self.image.resize((540, 495))
        self.image = ImageTk.PhotoImage(photo)
        self.label = Label(self.frame_solution, image=self.image)
        self.label.place(x=460, y=40)

        self.label_result = Label(self.frame_solution, text='Результат: ', font=self.label_font, bg=self.main_color)
        self.label_result.place(x=18, y=10)
        self.text_result = Text(self.frame_solution, bg='white', relief='raised', bd=1)
        self.text_result.place(x=20, y=40, width=420, height=500)





