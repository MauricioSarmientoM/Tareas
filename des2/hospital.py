from enum import Enum
from datetime import date
from tkinter.messagebox import showerror, showinfo, showwarning
class Specialty(Enum):
    Null = 0
    Pediatrics = 1
    Anesteology = 2
    Cardiology = 3
    Gastroenterology = 4
    General = 5
    Gynecology = 6
    Obstetrics = 7
    @classmethod
    def Validate(self, specialty : str):
        if specialty.lower() == 'pediatrics': return Specialty.Pediatrics
        elif specialty.lower() == 'anesteology': return Specialty.Anesteology
        elif specialty.lower() == 'cardiology': return Specialty.Cardiology
        elif specialty.lower() == 'gastroenterology': return Specialty.Gastroenterology
        elif specialty.lower() == 'general': return Specialty.General
        elif specialty.lower() == 'gynecology': return Specialty.Gynecology
        elif specialty.lower() == 'obstetrics': return Specialty.Obstetrics
        return Specialty.Null
class Area(Enum):
    Null = 0
    Extern = 1
    Emergency = 2
    Pediatrics = 3
    Operating = 4
    Hospitalization = 5
    ICU = 6
    @classmethod
    def Validate(self, area : str):
        if area.lower() == 'extern': return Area.Extern
        elif area.lower() == 'emergency': return Area.Emergency
        elif area.lower() == 'pediatrics': return Area.Pediatrics
        elif area.lower() == 'operating': return Area.Operating
        elif area.lower() == 'hospitalization': return Area.Hospitalization
        elif area.lower() == 'icu': return Area.ICU
        return Area.Null
class AFP(Enum):
    Null = 0
    Capital = 1
    Cuprum = 2
    Habitat = 3
    Modelo = 4
    Planvital = 5
    Provida = 6
    Uno = 7
    @classmethod
    def Validate(self, afp : str):
        if afp.lower() == 'capital': return AFP.Capital
        elif afp.lower() == 'cuprum': return AFP.Cuprum
        elif afp.lower() == 'habitat': return AFP.Habitat
        elif afp.lower() == 'modelo': return AFP.Modelo
        elif afp.lower() == 'planvital': return AFP.Planvital
        elif afp.lower() == 'provida': return AFP.Provida
        elif afp.lower() == 'uno': return AFP.Uno
        return AFP.Null
class Prevision(Enum):
    Null = 0
    FONASA = 1
    ISAPRE = 2
    Particular = 3
    @classmethod
    def Validate(self, prevision : str):
        if prevision.lower() == 'fonasa': return Prevision.FONASA
        elif prevision.lower() == 'isapre': return Prevision.ISAPRE
        elif prevision.lower() == 'particular': return Prevision.Particular
        return Prevision.Null
class Unit(Enum):
    Null = 0
    General = 1
    Personal = 2
    Chief = 3
    @classmethod
    def Validate(self, unit : str):
        if unit.lower() == 'general': return Unit.General
        elif unit.lower() == 'personal': return Unit.Personal
        elif unit.lower() == 'chief': return Unit.Chief
        return Unit.Null
class Derivation(Enum):
    Null = 0
    Consult = 1
    Emergency = 2
    @classmethod
    def Validate(self, derivation : str):
        if derivation.lower() == 'consult': return Derivation.Consult
        elif derivation.lower() == 'emergency': return Derivation.Emergency
        return Derivation.Null
class RUT():
    def __init__(self, rut : int) -> None:
        self.rut = rut
        data = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7]
        self.__digit = 11 - (sum([int(i) * j for i, j in zip(str(rut)[::-1], data)]) - int(sum([int(i) * j for i, j in zip(str(rut)[::-1], data)]) / 11) * 11)
    @property
    def digit(self):
        return f'{self.__digit}' if self.__digit < 10 else 'K' if self.__digit != 10 else '0'
    @classmethod
    def ValidateRut(self, rut : str) -> bool:
        try:
            if '-' in rut:
                parts = rut.split('-')
                rut = ''.join(parts[0].split('.'))
                theRealDeal = RUT(int(rut))
                if parts[1] == theRealDeal.digit:
                    return True
                else:
                    showwarning('Invalid', 'The validator number in this RUT is incorrect.')
                    return False
            else:
                showwarning('Invalid', 'The given RUT does not contains a hyphen with validator number.')
                return False
        except Exception as e:
            showerror('Error', e)
            return False
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
    def __init__(self, rut : RUT, name: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, afp: AFP = AFP.Uno, salary : int = 0) -> None:
        super().__init__(rut, name, admission, prevision, afp)
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
    def __init__(self, rut : RUT, name: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, salary: int = 0, afp: AFP = AFP.Uno, specialty : Specialty = Specialty.General, area : Area = Area.Null) -> None:
        super().__init__(rut, name, admission, prevision, afp, salary)
        self.specialty = specialty
        self.area = area
    @property
    def payment(self) -> float:
        return round(super().payment + self.salary * .05)
class Administrative(Worker):
    def __init__(self, rut : RUT, name: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, salary: int = 0, afp: AFP = AFP.Uno, unit : Unit = Unit.General) -> None:
        super().__init__(rut, name, admission, prevision, afp, salary)
        self.unit = unit
    @property
    def payment(self) -> float:
        return round(super().payment + self.salary * .03)
class Patient(Person):
    def __init__(self, rut : RUT, name: str = '', admission : date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, afp: AFP = AFP.Uno, reason : str = '', derivation : Derivation = Derivation.Consult) -> None:
        super().__init__(rut, name, admission, prevision, afp)
        self.reason = reason
        self.derivation = derivation
        self.medic : Medic = None
class Hospital():
    def __init__(self, name : str = 'hospital Regional Copiapo San Jose del Carmen', boxAmount : int = 5) -> None:
        self.name = name
        self.workers : list[Worker] = []
        self.box : list[Patient] = []
        self.waitList : list [Patient] = []
        self.boxAmount = boxAmount
    def Admit(self, patient : Patient) -> int:
        if len(self.box) < self.boxAmount:
            self.box.append(patient)
            return len(self.box)
        else:
            self.waitList.append(patient)
            return 0
    def Money(self, boxNumber : int = 0):
        if self.box[boxNumber] != None:
            pass
def Main():
    print(RUT(20751584))
    print(date(2000, 4, 15))
    print(date(2000, 4, 15).__str__())
    print(int(AFP.Habitat.value))
if __name__ == '__main__': Main()