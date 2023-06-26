from pymysql import connect
from tk import *
from enum import Enum
from datetime import date
class Specialty(Enum):
    Pediatrics = 0
    Anesteology = 1
    Cardiology = 2
    Gastroenterology = 3
    General = 4
    Gynecology = 5
    Obstetrics = 6
class Area(Enum):
    Extern = 0
    Emergency = 1
    Pediatrics = 2
    Operating = 3
    Hospitalization = 4
    ICU = 5
class Prevision(Enum):
    FONASA = 0
    ISAPRE = 1
    Particular = 2
class Person():
    def __init__(self, name : str = '', RUT : str = '', admission : date = date(year = 2023, month = 7, day = 3), prevision : Prevision = Prevision.FONASA) -> None:
        pass
class Medic(Person):

class DB():
    def __init__(self) -> None:
        try:
            self.cursor = connect(
                host='localhost',
                user= 'root',
                password='',
                db='dev2'
            ).cursor()
            print('Connected Succesfully!')
        except ConnectionError as e:
            print(e)
            self.cursor = None
    def Reconnect(self):
        try:
            self.cursor = connect(
                host='localhost',
                user= 'root',
                password='',
                db='dev2'
            ).cursor()
            print('Connected Succesfully!')
        except ConnectionError as e:
            print(e)
            self.cursor = None
        return self
def Main():
    db = DB()
if __name__ == '__main__':
    Main()