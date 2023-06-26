class Car:
    def __init__(self, door = 4, wheel = 4, brand = '', year = 2004, moving = False) -> None:
        self.door = door
        self.wheel = wheel
        self.brand = brand
        self.year = year
        self.moving = moving
    def TurnOn(self):
        print('The car goes broom broom.')
        return self
    def State(self):
        print(f'The car has {self.door} doors and {self.wheel} wheels.\nIs moving? {self.moving}')
        return self
    def Accelerate(self, moving):
        self.moving = moving
        if self.moving: print('Car goes broom!')
        else: print('Car goes down.')
        return self
    

myCar = Car(brand = 'HotWheels', door = 2, year = 1999)
print(f'Funny car has {myCar.wheel} wils')
myCar.TurnOn().State().Accelerate(True).Accelerate(False)