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
class Derivation(Enum):
    Consult = 0
    Emergency = 1
class RUT():
    def __init__(self, rut : int) -> None:
        self.rut = rut
        data = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7]
        self.__digit = 11 - (sum([int(i) * j for i, j in zip(str(rut)[::-1], data)]) - int(sum([int(i) * j for i, j in zip(str(rut)[::-1], data)]) / 11) * 11)
    @property
    def digit(self):
        return f'{self.__digit}' if self.__digit < 10 else 'K' if self.__digit != 10 else '0'
    def __str__(self):
        return f'{self.rut}-{self.digit}'
class Person():
    def __init__(self, rut : RUT, name : str = '', admission : date = date(year = 2023, month = 7, day = 3), prevision : Prevision = Prevision.FONASA, afp : AFP = AFP.Uno) -> None:
        self.name = name
        self.rut = rut
        self.admission = admission
        self.prevision = prevision
        self.afp = afp
class Worker(Person):
    def __init__(self, name: str = '', rut: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, afp: AFP = AFP.Uno, salary : int = 0) -> None:
        super().__init__(name, rut, admission, prevision, afp)
        self.salary = salary
    @property
    def payment(self) -> float:
        afpPercentage : float = .1
        match self.afp:
            case AFP.Capital | AFP.Cuprum: afpPercentage = .1144
            case AFP.Habitat: afpPercentage = .1127
            case AFP.Modelo: afpPercentage = .1058
            case AFP.Planvital: afpPercentage = .1116
            case AFP.Provida: afpPercentage = .1145
            case AFP.Uno: afpPercentage = .1069
        timeBonus : float = 0
        workTime : int = (date.today - self.admission).year
        if workTime > 20:
            timeBonus = .05
        elif workTime > 30:
            timeBonus = .07
        return self.salary - self.salary * afpPercentage - self.salary * .07 + self.salary + timeBonus
class Medic(Worker):
    def __init__(self, name: str = '', rut: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, salary: int = 0, afp: AFP = AFP.Uno, specialty : Specialty = Specialty.General, area : Area = Area.Null) -> None:
        super().__init__(name, rut, admission, prevision, afp, salary)
        self.specialty = specialty
        self.area = area
    @property
    def payment(self) -> float:
        return round(super().payment + self.salary * .05)
class Administrative(Worker):
    def __init__(self, name: str = '', rut: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, salary: int = 0, afp: AFP = AFP.Uno, unit : Unit = Unit.General) -> None:
        super().__init__(name, rut, admission, prevision, afp, salary)
        self.unit = unit
    @property
    def payment(self) -> float:
        return round(super().payment + self.salary * .03)
class Patient(Person):
    def __init__(self, name: str = '', rut: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, afp: AFP = AFP.Uno, reason : str = '', derivation : Derivation = Derivation.Consult) -> None:
        super().__init__(name, rut, admission, prevision, afp)
        self.reason = reason
        self.derivation = derivation
        self.medic : Medic = None
class Hospital():
    def __init__(self, name : str = 'Hospital Regional Copiapo San Jose del Carmen', boxAmount : int = 5) -> None:
        self.name = name
        self.box : list[Patient, None] = []
        if boxAmount >= 0:
            for i in range(boxAmount):
                self.box.append(None)
        else: self.box.append(None)
    def Admit(self, patient : Patient):
        pass
    def Money(self, boxNumber : int = 0):
        if self.box[boxNumber] != None:
            pass
def Main():
    print(RUT(20751584))
if __name__ == '__main__': Main()