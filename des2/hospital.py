from enum import Enum
from datetime import date
from tkinter import Event
from tkinter.messagebox import showerror, showinfo, showwarning, askquestion
from db import DB
from des2.db import DB
class WindowUIState(Enum):
    Medic = 0
    TENS = 1
    Admin = 2
    Patient = 3
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
    def InsertQuery(self, db : DB) -> DB:
        return db
    def UpdateQuery(self, db : DB, rut : int) -> DB:
        return db
    def DeleteQuery(self, db : DB, rut : int) -> DB:
        return db
class Worker(Person):
    def __init__(self, rut : RUT, name: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, afp: AFP = AFP.Uno, salary : int = 0) -> None:
        super().__init__(rut, name, admission, prevision, afp)
        self.salary = salary
    @property
    def afpDiscount(self) -> int:
        afpPercentage : float = .1
        match self.afp:
            case AFP.Capital | AFP.Cuprum: afpPercentage = .1144
            case AFP.Habitat: afpPercentage = .1127
            case AFP.Modelo: afpPercentage = .1058
            case AFP.Planvital: afpPercentage = .1116
            case AFP.Provida: afpPercentage = .1145
            case AFP.Uno: afpPercentage = .1069
        return round(self.salary * afpPercentage)
    @property
    def healthDiscount(self) -> int:
        return round(self.salary * .07)
    @property
    def bonus(self) -> int:
        timeBonus : float = 0
        workTime : int = (date.today - self.admission).year
        if workTime > 20:
            timeBonus = .05
        elif workTime > 30:
            timeBonus = .07
        return self.salary * timeBonus
    @property
    def payment(self) -> int:
        return self.salary - self.afpDiscount - self.healthDiscount + self.bonus
class Medic(Worker):
    def __init__(self, rut : RUT, name: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, afp: AFP = AFP.Uno, salary: int = 0, specialty : Specialty = Specialty.General) -> None:
        super().__init__(rut, name, admission, prevision, afp, salary)
        self.specialty = specialty
    @property
    def bonus(self) -> int:
        return super().bonus + round(self.salary * .05)
    def InsertQuery(self, db : DB) -> DB:
        return db.InsertTable(table = 'workers', column = 'rut name admission prevision afp salary specialty occupation', values = [self.rut.rut, self.name, self.admission.__str__(), self.prevision.value, self.afp.value, self.salary, self.specialty.value, 0])
    def UpdateQuery(self, db: DB, rut: int) -> DB:
        return db.UpdateSet(table = 'workers', column = 'rut name admission prevision afp salary specialty', values = [self.rut.rut, self.name, self.admission.__str__(), self.prevision.value, self.afp.value, self.salary, self.specialty.value], where = f'rut = {rut}')
class TENS(Medic):
    def __init__(self, rut : RUT, name: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, afp: AFP = AFP.Uno, salary: int = 0, specialty : Specialty = Specialty.General, area : Area = Area.Extern) -> None:
        super().__init__(rut, name, admission, prevision, afp, salary,)
        self.area = area
    def InsertQuery(self, db : DB) -> DB:
        return db.InsertTable(table = 'workers', column = 'rut name admission prevision afp salary specialty area occupation', values = [self.rut.rut, self.name, self.admission.__str__(), self.prevision.value, self.afp.value, self.salary, self.specialty.value, self.area.value, 1])
    def UpdateQuery(self, db: DB, rut: int) -> DB:
        return db.UpdateSet(table = 'workers', column = 'rut name admission prevision afp salary specialty area', values = [self.rut.rut, self.name, self.admission.__str__(), self.prevision.value, self.afp.value, self.salary, self.specialty.value, self.area.value], where = f'rut = {rut}')
class Administrative(Worker):
    def __init__(self, rut : RUT, name: str = '', admission: date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, afp: AFP = AFP.Uno, salary: int = 0, unit : Unit = Unit.General) -> None:
        super().__init__(rut, name, admission, prevision, afp, salary)
        self.unit = unit
    @property
    def bonus(self) -> int:
        return super().bonus + round(self.salary * .03)
    def InsertQuery(self, db: DB) -> DB:
        return db.InsertTable(table = 'workers', column = 'rut name admission prevision afp salary unit occupation', values = [self.rut.rut, self.name, self.admission.__str__(), self.prevision.value, self.afp.value, self.salary, self.unit.value, 2])
    def UpdateQuery(self, db: DB, rut : int) -> DB:
        return db.UpdateSet(table = 'person', column = 'rut name admission prevision afp salary unit', values = [self.rut.rut, self.name, self.admission.__str__(), self.prevision.value, self.afp.value, self.salary, self.unit.value], where = f'rut = {rut}')
class Patient(Person):
    def __init__(self, rut : RUT, name: str = '', admission : date = date(year=2023, month=7, day=3), prevision: Prevision = Prevision.FONASA, afp: AFP = AFP.Uno, reason : str = '', derivation : Derivation = Derivation.Consult) -> None:
        super().__init__(rut, name, admission, prevision, afp)
        self.reason = reason
        self.derivation = derivation
        self.medic : Medic = None
    def InsertQuery(self, db: DB) -> DB:
        return db.InsertTable(table = 'patients', column = 'rut name admission prevision afp reason derivation box occupation', values = [self.rut.rut, self.name, self.admission.__str__(), self.prevision.value, self.afp.value, self.reason, self.derivation.value, self.box, 3])
class Hospital(DB):
    def __init__(self, name : str = 'hospital Regional Copiapo San Jose del Carmen', boxAmount : int = 5, host : str = 'localhost', user : str = 'root', password : str = '', database : str = '') -> None:
        super().__init__(host, user, password, database)
        self.name = name
    def FreeBox(self) -> list:
        try:
            box = self.Select(table = 'patient')
            return [i for i in box]
        except Exception as e:
            showerror('Error', message = e)
            return []
    def SelectUpdateMedicTable(self, event : Event, items : dict, vars : dict):
        try:
            item = items['medicTable'].identify('item', event.x, event.y)
            rut = int(items['medicTable'].item(item, 'values')[0])
            data = self.Select(table = 'workers', fetch = 1, where = f'occupation = 1 AND rut = {rut}')
            vars['search'].set(RUT(data[0]).__str__())
            vars['rut'].set(RUT(data[0]).__str__())
            vars['name'].set(data[1])
            vars['year'].set(data[2].year)
            vars['month'].set(data[2].month)
            vars['day'].set(data[2].day)
            items['previsionCombobox'].set(data[3])
            items['afpCombobox'].set(data[4])
            vars['salary'].set(data[5])
            items['specialtyCombobox'].set(data[6])
            items['areaCombobox'].set(data[7])
        except Exception as e: showerror('Error', message = e)
    def SelectUpdateAdminTable(self, event : Event, items : dict, vars : dict):
        try:
            item = items['adminTable'].identify('item', event.x, event.y)
            rut = int(items['adminTable'].item(item, 'values')[0])
            data = self.Select(table = 'workers', fetch = 1, where = f'occupation = 2 AND rut = {rut}')
            vars['search'].set(RUT(data[0]).__str__())
            vars['rut'].set(RUT(data[0]).__str__())
            vars['name'].set(data[1])
            vars['year'].set(data[2].year)
            vars['month'].set(data[2].month)
            vars['day'].set(data[2].day)
            items['previsionCombobox'].set(data[3])
            items['afpCombobox'].set(data[4])
            vars['salary'].set(data[5])
            items['unitCombobox'].set(data[8])
        except Exception as e: showerror('Error', message = e)
    def SelectUpdatePatientTable(self, event : Event, items : dict, vars : dict):
        try:
            item = items['patientTable'].identify('item', event.x, event.y)
            rut = int(items['patientTable'].item(item, 'values')[0])
            data = self.Select(table = 'patients', fetch = 1, where = f'occupation = 3 AND rut = {rut}')
            vars['search'].set(RUT(data[0]).__str__())
            vars['rut'].set(RUT(data[0]).__str__())
            vars['name'].set(data[1])
            vars['year'].set(data[2].year)
            vars['month'].set(data[2].month)
            vars['day'].set(data[2].day)
            items['previsionCombobox'].set(data[3])
            items['afpCombobox'].set(data[4])
            vars['reason'].set(data[9])
            items['derivationCombobox'].set(data[10])
        except Exception as e: showerror('Error', message = e)
    def InsertPersonTable(self, state : WindowUIState, ClearItems, items : dict, vars : dict):
        try:
            if RUT.ValidateRut(str(vars['rut'].get())):
                person = Person()
                if state == WindowUIState.Medic: person = Medic(name = vars['name'].get(), rut = RUT(int(''.join(str(vars['rut'].get()).split('-')[0].split('.')))), admission = date(vars['year'].get(), vars['month'].get(), vars['day'].get()), afp = AFP.Validate(items['afpCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()), prevision = Prevision.Validate(items['previsionCombobox'].get()), salary = vars['salary'].get(), specialty = Specialty.Validate(items['specialtyCombobox'].get()))
                elif state == WindowUIState.TENS: person = TENS(name = vars['name'].get(), rut = RUT(int(''.join(str(vars['rut'].get()).split('-')[0].split('.')))), admission = date(vars['year'].get(), vars['month'].get(), vars['day'].get()), afp = AFP.Validate(items['afpCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()), prevision = Prevision.Validate(items['previsionCombobox'].get()), salary = vars['salary'].get(), specialty = Specialty.Validate(items['specialtyCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()))
                elif state == WindowUIState.Admin: person = Administrative(name = vars['name'].get(), rut = RUT(int(''.join(str(vars['rut'].get()).split('-')[0].split('.')))), admission = date(vars['year'].get(), vars['month'].get(), vars['day'].get()), afp = AFP.Validate(items['afpCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()), prevision = Prevision.Validate(items['previsionCombobox'].get()), salary = vars['salary'].get(), unit = Unit.Validate(items['unitCombobox'].get()))
                elif state == WindowUIState.Patient: person = Patient(name = vars['name'].get(), rut = RUT(int(''.join(str(vars['rut'].get()).split('-')[0].split('.')))), admission = date(vars['year'].get(), vars['month'].get(), vars['day'].get()), afp = AFP.Validate(items['afpCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()), prevision = Prevision.Validate(items['previsionCombobox'].get()), reason = vars['reason'].get(), derivation = Derivation.Validate(items['derivationCombobox'].get()))
                person.InsertQuery(self)
                ClearItems()
        except Exception as e: showerror('Error', message = e)
    def UpdatePersonTable(self, state : WindowUIState, ClearItems, items : dict, vars : dict):
        try:
            if RUT.ValidateRut(str(vars['search'].get())):
                medic : Medic = None
                rut = int(''.join(str(vars['search'].get()).split('-')[0].split('.')))
                for i in self.hospital.workers:
                    if i.rut.rut == rut:
                        medic = i
                        rut = i.rut.rut
                        break
                if not medic is None:
                    person = Person()
                    if state == WindowUIState.Medic: person = Medic(name = vars['name'].get(), rut = RUT(int(''.join(str(vars['rut'].get()).split('-')[0].split('.')))), admission = date(vars['year'].get(), vars['month'].get(), vars['day'].get()), afp = AFP.Validate(items['afpCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()), prevision = Prevision.Validate(items['previsionCombobox'].get()), salary = vars['salary'].get(), specialty = Specialty.Validate(items['specialtyCombobox'].get()))
                    elif state == WindowUIState.TENS: person = TENS(name = vars['name'].get(), rut = RUT(int(''.join(str(vars['rut'].get()).split('-')[0].split('.')))), admission = date(vars['year'].get(), vars['month'].get(), vars['day'].get()), afp = AFP.Validate(items['afpCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()), prevision = Prevision.Validate(items['previsionCombobox'].get()), salary = vars['salary'].get(), specialty = Specialty.Validate(items['specialtyCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()))
                    elif state == WindowUIState.Admin: person = Administrative(name = vars['name'].get(), rut = RUT(int(''.join(str(vars['rut'].get()).split('-')[0].split('.')))), admission = date(vars['year'].get(), vars['month'].get(), vars['day'].get()), afp = AFP.Validate(items['afpCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()), prevision = Prevision.Validate(items['previsionCombobox'].get()), salary = vars['salary'].get(), unit = Unit.Validate(items['unitCombobox'].get()))
                    elif state == WindowUIState.Patient: person = Patient(name = vars['name'].get(), rut = RUT(int(''.join(str(vars['rut'].get()).split('-')[0].split('.')))), admission = date(vars['year'].get(), vars['month'].get(), vars['day'].get()), afp = AFP.Validate(items['afpCombobox'].get()), area = Area.Validate(items['areaCombobox'].get()), prevision = Prevision.Validate(items['previsionCombobox'].get()), reason = vars['reason'].get(), derivation = Derivation.Validate(items['derivationCombobox'].get()))
                    person.InsertQuery(self)
                    ClearItems()
        except Exception as e: showerror('Error', message = e)
    def DeletePersonTable(self, table : str, state : WindowUIState, ClearItems, items : dict, vars : dict):
        try:
            if RUT.ValidateRut(str(vars['search'].get())):
                rut = int(''.join(str(vars['search'].get()).split('-')[0].split('.')))
                if state != WindowUIState.Patient: self.DeleteTable(table = 'remunerations', where = f'fkPerson = {rut}')
                self.DeleteTable(table = table, where = f'occupation = {state.value} AND rut = {rut}')
                ClearItems()
        except Exception as e: showerror('Error', message = e)
    def AskIfDelete(self, state : WindowUIState, ClearItems, items : dict, vars : dict):
        profession = ''
        if state == WindowUIState.Medic: profession = 'Medic'
        elif state == WindowUIState.TENS: profession = 'TENS'
        elif state == WindowUIState.Admin: profession = 'Administrative'
        elif state == WindowUIState.Patient: profession = 'Patient'
        if askquestion('Delete', f'{vars["name"].get()}, a {profession} will be deleted from the system along all their data, are you sure?') == 'yes':
            self.DeletePersonTable(state, ClearItems, items, vars)
def Main():
    print(RUT(20751584))
    print(date(2000, 4, 15))
    print(date(2000, 4, 15).__str__())
    print(int(AFP.Habitat.value))
if __name__ == '__main__': Main()