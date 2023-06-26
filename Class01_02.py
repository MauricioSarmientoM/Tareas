class Ball:
    def __init__(self, moving = False) -> None:
        self.moving = moving
    def Move(self, moving):
        self.moving = moving
        print('The ball is {}moving.'.format(self.moving if '' else 'not '))
        return self
class Person:
    def __init__(self, name = 'Hugh Man', id = 0, health = 10) -> None:
        self.name = name
        self.id = id
        self.health = self.maxHealth = health
    def __repr__(self):
        return f'Name: {self.name}\nID: {self.id}'
class Player(Person):
    def __init__(self, name = 'Hugh Man', id = 0, position = 'Attack') -> None:
        super().__init__(name, id)
        self.position = 'Attack'
    def Kick(self, target):
        if type(target) == type(Player):
            target.TakeDamage()
        else:
            target.Move(True)
        return self
    def TakeDamage(self):
        return self