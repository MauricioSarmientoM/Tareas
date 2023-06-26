from pymysql import connect
from des2.main import AFP, Prevision
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
    Null = 0
    Extern = 1
    Emergency = 2
    Pediatrics = 3
    Operating = 4
    Hospitalization = 5
    ICU = 6
class AFP(Enum):
    Capital = 0
    Cuprum = 1
    Habitat = 2
    Modelo = 3
    Planvital = 4
    Provida = 5
    Uno = 6
class Prevision(Enum):
    FONASA = 0
    ISAPRE = 1
    Particular = 2
class Unit(Enum):
    General = 0
    Personal = 1
    Chief = 2
class Person():
    def __init__(self, name : str = '', rut : str = '', admission : date = date(year = 2023, month = 7, day = 3), prevision : Prevision = Prevision.FONASA, salary : int = 0, afp : AFP = AFP.Uno) -> None:
        self.name = name
        self.rut = rut
        self.admission = admission
        self.prevision = prevision
        self.salary = salary
        self.afp = afp
    @property
    def payment(self) -> int:
        afpPercentage : float = .1
        match self.afp:
            case AFP.Capital | AFP.Cuprum: afpPercentage = .1144
            case AFP.Habitat: afpPercentage = .1127
            case AFP.Modelo: afpPercentage = .1058
            case AFP.Planvital: afpPercentage = .1116
            case AFP.Provida: afpPercentage = .1145
            case AFP.Uno: afpPercentage = .1069
        return self.salary - self.salary * afpPercentage - self.salary * .07
class Medic(Person):
    def __init__(self, name: str = '', rut: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, salary: int = 0, afp: AFP = AFP.Uno, specialty : Specialty = Specialty.General, area : Area = Area.Null) -> None:
        super().__init__(name, rut, admission, prevision, salary, afp)
        self.specialty = specialty
        self.area = area
class Administrative(Person):
    def __init__(self, name: str = '', rut: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, salary: int = 0, afp: AFP = AFP.Uno, unit : Unit = Unit.General) -> None:
        super().__init__(name, rut, admission, prevision, salary, afp)
        self.unit = unit
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