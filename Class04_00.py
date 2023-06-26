from typing import Self
from random import choice, randint, uniform

class Person:
    def __init__(self, name : str = 'Euphemia', age : int = 38):
        self.__name = name
        self.__age = age

    @property
    def name(self) -> str: return self.__name
    @name.setter
    def name(self, name : str) -> str:
        self.__name = name
        return self.__name
    @property
    def age(self) -> str: return self.__age
    @age.setter
    def age(self, age : int) -> int:
        self.__age = age
        return self.__age
    @property
    def printPerson(self) -> str: return f'{self.name} has {self.age}'
    @property
    def isLegal(self) -> bool: return self.age >= 18
    def __gt__(self, other : Self) -> bool: return self.age > other.age

def main():
    data = 'names.txt'
    Complete = lambda x, y : ''.join(list(x[::-1] + '0' * ((y - len(x) % y) if y != len(x) else 0))[::-1])
    RandomName = lambda x : choice(list(open(x))).replace('\n', '')
    RandomRut = lambda : '.'.join([str(randint(7, 25)), Complete(str(randint(0, 999)), 3), Complete(str(randint(0, 999)), 3)]) + '-' + str(randint(1, 9))
    RutToAge = lambda x : round(100 - (uniform(.9, 1.1) * float(x.split('-')[0].split('.')[0]) * 3.5 ))
    people = {}
    ruts = [RandomRut() for i in range(100)]
    for i in ruts:
        people[i] = Person(RandomName(data), RutToAge(i))
    for i in range(100):
        option = randint(1, 3)
        rut = choice(list(people.keys()))
        if option == 1:
            print(f'{people[rut].printPerson}, has 18 or more years old, so is legal' if people[rut].isLegal else f'{people[rut].printPerson}, has less than 18 years old, so is a minor.')
        elif option == 2:
            other = people[choice(list(people.keys()))]
            print(f'{people[rut].printPerson}, and {other.printPerson}, so {people[rut].name} is older than {other.name}' if people[rut] > other else f'{people[rut].printPerson}, and {other.printPerson}, so {people[rut].name} is not older than {other.name}')
        elif option == 3:
            print(people[rut].printPerson)

if __name__ == '__main__':
    main()
