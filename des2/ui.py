from tkinter import Tk
from hospital import Hospital
from db import DB
class UI():
    def __init__(self, hospital : Hospital, db : DB) -> None:
        self.window = Tk()
        self.window.title(hospital.name)
        self.window.geometry('600x400')
    def AdminMedics(self):
        pass
    def Render(self):
        self.window.mainloop()