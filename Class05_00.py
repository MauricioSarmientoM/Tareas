from typing import Self
from random import choice, randint, uniform
from enum import Enum
class State(Enum):
    Single = 0
    Married = 1
    Widow = 2
class Level(Enum):
    First1 = 101; First2 = 102; Second1 = 201; Second2 = 202; Third1 = 301; Third2 = 302; Fourth1 = 401; Fourth2 = 402; Fifth1 = 501; Fifth2 = 502; Sixth1 = 601; Sixth2 = 602
class Department(Enum):
    Industry = 0; Comercial = 1; Informatic = 2; Metalurgy = 3; Mines = 4; Geology = 5
class Section(Enum):
    Library = 0; Deanery = 1; Secretary = 2; Academic = 3
class Person:
    def __init__(self, name : str = '', surname : str = '', rut : str = '', year : int = 2000, state : State = State(0)) -> None:
        self.name = name
        self.surname = surname
        self.rut = rut
        self.year = year
        self.state = state
    def ChangeState(self, state : State = State(0)) -> Self:
        self.state = state
        return self
    def __str__(self) -> str:
        return f'\tName: {self.name} {self.surname}\n\tRut: {self.rut}\n\tBirth date: {self.year}\n\tCivil State: {self.state.name}'
class Student(Person):
    def __init__(self, name : str = '', surname : str = '', rut : str = '', year : int = 2000, state : State = State(0), level : Level = Level(101)) -> None:
        super().__init__(name = name, surname = surname, rut = rut, year = year, state = state)
        self.level = level
    def Enroll(self, leAvel : Level = Level(101)) -> Self:
        self.level = level
        return self
    def __str__(self) -> str:
        return super().__str__() + f'\n\tStudent Level: {self.level.value}'
class Professor(Person):
    def __init__(self, name : str = '', surname : str = '', rut : str = '', year : int = 2000, state : State = State(0), department : Department = Department(0)) -> None:
        super().__init__(name = name, surname = surname, rut = rut, year = year, state = state)
        self.department = department
    def ChangeDepartment(self, department : Department = Department(0)) -> Self:
        self.department = department
        return self
    def __str__(self) -> str:
        return super().__str__() + f'\n\tProfessor Department: {self.department.name}'
class CleaningPersonal(Person):
    def __init__(self, name : str = '', surname : str = '', rut : str = '', year : int = 2000, state : State = State(0), section : Section = Section(0)) -> None:
        super().__init__(name = name, surname = surname, rut = rut, year = year, state = state)
        self.section = section
    def ChangeSection(Self, section : Section = Section(0)) -> Self:
        self.section = section
    def __str__(self) -> str:
        return super().__str__() + f'\n\tCleaning Section: {self.section.name}'

def CreateRandom(people):
    names = 'names.txt'
    surnames = 'surnames.txt'
    Complete = lambda x, y : ''.join(list(x[::-1] + '0' * ((y - len(x) % y) if y != len(x) else 0))[::-1])
    RandomName = lambda x : choice(list(open(x))).replace('\n', '').lower().capitalize()
    RandomRut = lambda : '.'.join([str(randint(7, 25)), Complete(str(randint(0, 999)), 3), Complete(str(randint(0, 999)), 3)]) + '-' + str(randint(1, 9))
    RutToAge = lambda x : round(100 - (uniform(.9, 1.1) * float(x.split('-')[0].split('.')[0]) * 3.5 ))
    try:
        amount = int(input('How many random people do you need?\n'))
        ruts = [RandomRut() for i in range(amount)]
        for i in ruts:
            option = randint(0, 2)
            match option:
                case 0:
                    people.append(Student(RandomName(names), RandomName(surnames), i, 2030 - RutToAge(i), State(0) if RutToAge(i) < 23 else choice(list(State)), choice(list(Level))))
                case 1:
                    people.append(Professor(RandomName(names), RandomName(surnames), i, 2030 - RutToAge(i), State(0) if RutToAge(i) < 23 else choice(list(State)), choice(list(Department))))
                case 2:
                    people.append(CleaningPersonal(RandomName(names), RandomName(surnames), i, 2030 - RutToAge(i), State(0) if RutToAge(i) < 23 else choice(list(State)), choice(list(Section))))
    except: print(f'{amount} isn\'n a valid amount.')
def ShowPeople(people : list[Person], option : str) -> None:
    for i, j in enumerate(people):
        match option.split(' '):
            case ['all']:
                print(f'{i + 1}) {j}')
            case ['name']:
                print(f'{i + 1}) {j.name}')
            case _:
                print('?')
def ModifyPeople(people : list[Person]) -> None:
    ShowPeople(people, 'name')
    try:
        option = int(input('Which person do you want to modify?\n'))
        modify = people[option - 1]
        if isinstance(modify, Student):
            print('Choose a new level to enroll the student.\n')
            for i, j in enumerate(list(Level)): print(f'{i + 1}) {j.value}')
        elif isinstance(modify, Professor): 
            print('Choose a new department to move the professor.\n')
            for i, j in enumerate(list(Department)): print(f'{i + 1}) {j.name}')
        elif isinstance(modify, CleaningPersonal):
            print('Choose a new section to move the cleaning personal.\n')
            for i, j in enumerate(list(Section)): print(f'{i + 1}) {j.name}')
        option = int(input())
        if isinstance(modify, Student): modify.Enroll(list(Level)[option - 1])
        elif isinstance(modify, Professor): modify.ChangeDepartment(Department(option - 1))
        elif isinstance(modify, CleaningPersonal): modify.ChangeSection(Section(option - 1))
    except: print(f'{option} is not a valid option')
def main(): 
    people = []
    print('University System')
    while True:
        option = input('Choose an option to proceed:\n\t1) Add People to the list\n\t2) Modify People from the list\n\t3) Show People from the list\n\t0) Exit\n')
        match option:
            case '0':
                print('Exiting...\n')
                break
            case '1': CreateRandom(people)
            case '2': ModifyPeople(people)
            case '3': ShowPeople(people, 'all')
            case _: print('Non valid option.\n')


if __name__ == '__main__':
    main()
